from transformers import pipeline
import torch
from PIL import Image
import cv2
import numpy as np

class AnalysisService:
    def __init__(self):
        # Metin analizi için model - Anahtar kelime çıkarma
        self.text_analyzer = pipeline("zero-shot-classification", 
                                    model="facebook/bart-large-mnli")
        
        # Görsel analizi için model - Daha güçlü nesne ve sahne tanıma
        self.image_analyzer = pipeline("image-classification", 
                                     model="microsoft/resnet-50")
        
        # Video analizi için model - Şiddet ve tehlikeli içerik tespiti
        self.video_analyzer = pipeline("video-classification", 
                                     model="facebook/timesformer-base-finetuned-k400")

    def analyze_text(self, text):
        """
        Metin analizi yapar ve anahtar kelimeleri döndürür
        """
        try:
            # Önemli kategorileri tanımlıyoruz
            candidate_labels = [
                # Products & Services
                "technology", "electronics", "smartphone", "computer", "software",
                "fashion", "clothing", "accessories", "beauty", "cosmetics",
                "food", "restaurant", "cooking", "beverage", "snack",
                "automotive", "car", "vehicle", "transportation", "travel",
                
                # Activities & Interests
                "sports", "fitness", "exercise", "health", "wellness",
                "entertainment", "movie", "music", "game", "art",
                "education", "learning", "study", "course", "training",
                
                # Business & Finance
                "business", "finance", "investment", "marketing", "advertising",
                "real estate", "property", "housing", "construction", "architecture",
                
                # Lifestyle & Social
                "lifestyle", "fashion", "beauty", "health", "wellness",
                "social", "community", "relationship", "family", "friendship"
            ]
            
            results = self.text_analyzer(text, candidate_labels, multi_label=True)
            
            # Sadece yüksek güvenilirlikli etiketleri alıyoruz
            labels = [
                {"label": label, "score": score}
                for label, score in zip(results["labels"], results["scores"])
                if score > 0.6  # Güven eşiği %60'a yükseltildi
            ]
            
            return {
                "success": True,
                "labels": labels
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def analyze_image(self, image_path):
        """
        Görsel analizi yapar ve etiketleri döndürür
        """
        try:
            image = Image.open(image_path)
            results = self.image_analyzer(image)
            
            # Sadece yüksek güvenilirlikli etiketleri alıyoruz
            labels = [
                {"label": result["label"], "score": result["score"]}
                for result in results
                if result["score"] > 0.1  # Güven eşiği
            ]
            
            return {
                "success": True,
                "labels": labels
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def analyze_video(self, video_path):
        """
        Video analizi yapar ve etiketleri döndürür
        """
        try:
            results = self.video_analyzer(video_path)
            
            # Sadece yüksek güvenilirlikli etiketleri alıyoruz
            labels = [
                {"label": result["label"], "score": result["score"]}
                for result in results
                if result["score"] > 0.05  # Daha düşük güven eşiği
            ]
            
            return {
                "success": True,
                "labels": labels
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 