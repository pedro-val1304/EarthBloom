# utils/pollinator_movement.py
import random

def predict_pollinator_flow(date):
    """Simula desplazamiento direccional de polinizadores."""
    directions = ["N", "S", "E", "W", "NE", "NW", "SE", "SW"]
    flow = [{"direction": random.choice(directions),
             "speed_kmh": round(random.uniform(1, 5), 1)} for _ in range(10)]
    return {"flows": flow}