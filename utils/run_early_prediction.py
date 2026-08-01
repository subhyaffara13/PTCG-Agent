import os
import random
import logging

logger = logging.getLogger(__name__)

def run_early_prediction(deck_a: list, deck_b: list, steps_dump: list, winner: str) -> str:
    prediction = "n/a"
    try:
        from factory.early_predictor import EarlyWinPredictor
        predictor = EarlyWinPredictor()
        prediction = predictor.predict_winner(deck_a, deck_b, steps_dump)
        if os.environ.get("IS_WORKER") != "true":
            if prediction != winner and winner in ("player_a", "player_b"):
                predictor.upgrade(prediction, winner, steps_dump)
    except Exception as e:
        logger.error(f"EarlyWinPredictor failed: {e}")
    return prediction
