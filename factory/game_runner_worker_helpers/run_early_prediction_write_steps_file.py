from . import Path, json, logger, os

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

def write_steps_file(log_dir: str, timestamp_str: str, label: str, v_a: str, v_b: str, steps_dump: list):
    steps_filename = f"steps_{timestamp_str}_{label}_v{v_a}_vs_v{v_b}.json"
    if os.environ.get("SKIP_GAME_LOGS") == "1":
        return steps_filename
    steps_path = Path(log_dir) / steps_filename
    
    final_rewards = [0.0, 0.0]
    if steps_dump and len(steps_dump[-1]) >= 2:
        final_rewards = [
            steps_dump[-1][0].get("reward") or 0.0,
            steps_dump[-1][1].get("reward") or 0.0
        ]
        
    replay_data = {
        "steps": steps_dump,
        "rewards": final_rewards,
        "info": {
            "TeamNames": [v_a, v_b]
        }
    }
    
    try:
        steps_path.write_text(json.dumps(replay_data, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to write steps file {steps_path}: {e}")
    return steps_filename

