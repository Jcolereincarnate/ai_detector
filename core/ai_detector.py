from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class AIContentDetector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIContentDetector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.model_name = "Mohinikathro/AI-Content-Detector"
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        print(f"Loading AI detector model: {self.model_name}")
        print(f" Device: {self.device}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            self.model.to(self.device)
            self.model.eval()
            
            self._initialized = True
            print(f" Model loaded successfully!")
            
        except Exception as e:
            print(f" Error loading model: {str(e)}")
            self._initialized = False
            raise
    
    def _chunk_text(self, text, max_words=150):
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i:i+max_words])
            chunks.append(chunk)
        return chunks
    
    def detect(self, text):
        if not text or len(text.strip()) == 0:
            return {
                "success": False,
                "error": "Text is empty",
                "prediction": None,
                "confidence": 0,
                "ai_percentage": 0
            }
        
        text = " ".join(text.strip().split())
        chunks = self._chunk_text(text, max_words=150)
        
        if len(chunks) == 0:
            return {
                "success": False,
                "error": "Text is too short or empty after preprocessing",
                "prediction": None,
                "confidence": 0,
                "ai_percentage": 0
            }
        
        ai_count = 0
        human_count = 0
        total_confidence = 0
        prob_sum = {"AI-Generated": 0, "Human-Written": 0}
        
        label_map = {0: "Human-Written", 1: "AI-Generated"}
        
        for chunk in chunks:
            try:
                inputs = self.tokenizer(
                    chunk,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=512
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    logits = outputs.logits
                    probs = torch.softmax(logits, dim=1)
                    
                    predicted_class = torch.argmax(probs, dim=1).item()
                    confidence = probs[0][predicted_class].item()
                    
                    probs_list = probs[0].tolist()
                    ai_prob = probs_list[1] if len(probs_list) > 1 else 0
                    human_prob = probs_list[0] if len(probs_list) > 0 else 0
            except Exception as e:
                ai_prob = 0
                human_prob = 0
                confidence = 0
                predicted_class = 0
            
            prediction = label_map.get(predicted_class, "Uncertain")
            if prediction == "AI-Generated":
                ai_count += 1
            elif prediction == "Human-Written":
                human_count += 1
            
            total_confidence += confidence
            prob_sum["AI-Generated"] + ai_prob
            prob_sum["Human-Written"] += human_prob
        
        total_chunks = len(chunks)
        ai_percentage = (ai_count / total_chunks) * 100
        avg_confidence = (total_confidence / total_chunks) * 100
        prob_avg = {k: round(v / total_chunks * 100, 2) for k, v in prob_sum.items()}
        
        overall_prediction = "AI-Generated" if ai_percentage >= 50 else "Human-Written"
        if avg_confidence < 0.6:
            overall_prediction = "Uncertain"
        
        return {
            "success": True,
            "prediction": overall_prediction,
            "confidence": round(avg_confidence, 2),
            "probabilities": prob_avg,
            "ai_percentage": round(ai_percentage, 2)
        }