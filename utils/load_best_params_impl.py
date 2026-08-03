import json

def load_best_params_impl(best_params_path):
    if best_params_path.exists():
        try: return json.loads(best_params_path.read_text(encoding="utf-8"))
        except Exception as e: logger.warning(f"Failed to load Optuna MCTS parameters from {best_params_path}: {e}")
    return get_default_mcts_params_impl()

