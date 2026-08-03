import json

def save_best_params_impl(best_params_path, params):
    try:
        best_params_path.parent.mkdir(parents=True, exist_ok=True)
        best_params_path.write_text(json.dumps(params, indent=2), encoding="utf-8")
        logger.info(f"Saved best Optuna MCTS parameters to {best_params_path}")
    except Exception as e:
        logger.warning(f"Failed to save best Optuna MCTS parameters: {e}")

