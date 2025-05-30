from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import gc
import os
import warnings
import logging
from functools import lru_cache

# HuggingFace uyarılarını kapat
warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger("transformers").setLevel(logging.ERROR)

class AnalysisService:
    def __init__(self):
        self._text_analyzer = None
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Model önbellek dizini
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'model_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Model yükleme zaman aşımı (saniye)
        self.model_timeout = 300  # 5 dakika
        
    def _unload_model(self):
        """Modeli bellekten kaldır"""
        if self._text_analyzer is not None:
            del self._text_analyzer
            self._text_analyzer = None
        self._clear_memory()
        
    @lru_cache(maxsize=1)
    def _load_text_analyzer(self):
        if self._text_analyzer is None:
            # Daha küçük ve hızlı bir model kullanıyoruz
            model_name = "distilbert-base-uncased-mnli"
            tokenizer = AutoTokenizer.from_pretrained(
                model_name, 
                cache_dir=self.cache_dir,
                local_files_only=False,
                resume_download=True
            )
            model = AutoModelForSequenceClassification.from_pretrained(
                model_name, 
                cache_dir=self.cache_dir,
                local_files_only=False,
                resume_download=True
            )
            self._text_analyzer = pipeline(
                "zero-shot-classification", 
                model=model,
                tokenizer=tokenizer,
                device=self.device
            )
        return self._text_analyzer

    def _clear_memory(self):
        """Belleği temizle ve GPU önbelleğini boşalt"""
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

    def analyze_text(self, text):
        try:
            text_analyzer = self._load_text_analyzer()
            
            # Metni cümlelere ayır
            sentences = text.split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Cümleleri küçük gruplara böl (batch processing)
            batch_size = 5
            all_labels = []
            
            for i in range(0, len(sentences), batch_size):
                batch = sentences[i:i + batch_size]
                
                for sentence in batch:
                    candidate_labels = [
                        "technology", "business", "entertainment", "sports", "health",
                        "education", "science", "politics", "environment", "lifestyle"
                    ]
                    
                    with torch.no_grad():
                        results = text_analyzer(sentence, candidate_labels, multi_label=True)
                    
                    sentence_labels = [
                        {"label": label, "score": score}
                        for label, score in zip(results["labels"], results["scores"])
                        if score > 0.6
                    ]
                    
                    if sentence_labels:
                        all_labels.extend(sentence_labels)
                
                # Her batch sonrası bellek temizliği
                self._clear_memory()
            
            # Tekrar eden etiketleri birleştir
            label_scores = {}
            for label in all_labels:
                if label["label"] not in label_scores or label["score"] > label_scores[label["label"]]:
                    label_scores[label["label"]] = label["score"]
            
            final_labels = [
                {"label": label, "score": score}
                for label, score in label_scores.items()
            ]
            
            final_labels.sort(key=lambda x: x["score"], reverse=True)
            
            # İşlem bittikten sonra modeli kaldır
            self._unload_model()
            
            return {
                "success": True,
                "labels": final_labels
            }
        except Exception as e:
            self._unload_model()
            return {
                "success": False,
                "error": str(e)
            } 