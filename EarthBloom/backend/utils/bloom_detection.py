# utils/bloom_detection.py
import random

def get_bloom_probability(aoi, date=None, season=None):
    """Simula la probabilidad de floración en cada celda del AOI"""
    features = []
    for feature in aoi["features"]:
        prob = random.uniform(0.3, 0.95)  # valor ejemplo
        feature["properties"] = {"bloom_probability": round(prob, 2)}
        features.append(feature)
        
    return {"type": "FeatureCollection", "features": features}