from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer, AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import cv2
import numpy as np
import gc
import os
import warnings
import logging

# HuggingFace uyarılarını kapat
warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger("transformers").setLevel(logging.ERROR)

class AnalysisService:
    def __init__(self):
        self.text_analyzer = None
        self.image_analyzer = None
        self.video_analyzer = None
        self.device = 0 if torch.cuda.is_available() else -1
        
        # Model önbellek dizini
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'model_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def _load_text_analyzer(self):
        if self.text_analyzer is None:
            model_name = "facebook/bart-large-mnli"
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
            self.text_analyzer = pipeline(
                "zero-shot-classification", 
                model=model,
                tokenizer=tokenizer,
                device=self.device
            )
        return self.text_analyzer
        
    def _load_image_analyzer(self):
        if self.image_analyzer is None:
            model_name = "microsoft/resnet-50"
            processor = AutoImageProcessor.from_pretrained(
                model_name, 
                cache_dir=self.cache_dir,
                local_files_only=False,
                resume_download=True
            )
            model = AutoModelForImageClassification.from_pretrained(
                model_name, 
                cache_dir=self.cache_dir,
                local_files_only=False,
                resume_download=True
            )
            self.image_analyzer = pipeline(
                "image-classification", 
                model=model,
                image_processor=processor,
                device=self.device
            )
        return self.image_analyzer
        
    def _load_video_analyzer(self):
        if self.video_analyzer is None:
            model_name = "facebook/timesformer-base-finetuned-k400"
            self.video_analyzer = pipeline(
                "video-classification", 
                model=model_name,
                device=self.device,
                cache_dir=self.cache_dir,
                local_files_only=False,
                resume_download=True
            )
        return self.video_analyzer

    def _clear_memory(self):
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
            
            all_labels = []
            
            for sentence in sentences:
                # Her cümle için genel kategorileri kullan
                candidate_labels = [
                    "technology", "business", "entertainment", "sports", "health",
                    "education", "science", "politics", "environment", "lifestyle"
                ]
                
                with torch.no_grad():
                    results = text_analyzer(sentence, candidate_labels, multi_label=True)
                
                # Yüksek güvenilirlikli etiketleri al
                sentence_labels = [
                    {"label": label, "score": score}
                    for label, score in zip(results["labels"], results["scores"])
                    if score > 0.6
                ]
                
                if sentence_labels:
                    all_labels.extend(sentence_labels)
            
            # Tekrar eden etiketleri birleştir ve en yüksek skorları al
            label_scores = {}
            for label in all_labels:
                if label["label"] not in label_scores or label["score"] > label_scores[label["label"]]:
                    label_scores[label["label"]] = label["score"]
            
            final_labels = [
                {"label": label, "score": score}
                for label, score in label_scores.items()
            ]
            
            # Skorlara göre sırala
            final_labels.sort(key=lambda x: x["score"], reverse=True)
            
            self._clear_memory()
            return {
                "success": True,
                "labels": final_labels
            }
        except Exception as e:
            self._clear_memory()
            return {
                "success": False,
                "error": str(e)
            }

    def analyze_image(self, image_path):
        try:
            image_analyzer = self._load_image_analyzer()
            image = Image.open(image_path)
            
            with torch.no_grad():
                results = image_analyzer(image)
            
            labels = [
                {"label": result["label"], "score": result["score"]}
                for result in results
                if result["score"] > 0.1
            ]
            
            self._clear_memory()
            return {
                "success": True,
                "labels": labels
            }
        except Exception as e:
            self._clear_memory()
            return {
                "success": False,
                "error": str(e)
            }

    def analyze_video(self, video_path):
        try:
            video_analyzer = self._load_video_analyzer()
            
            with torch.no_grad():
                results = video_analyzer(video_path)
            
            labels = [
                {"label": result["label"], "score": result["score"]}
                for result in results
                if result["score"] > 0.05
            ]
            
            self._clear_memory()
            return {
                "success": True,
                "labels": labels
            }
        except Exception as e:
            self._clear_memory()
            return {
                "success": False,
                "error": str(e)
            } 