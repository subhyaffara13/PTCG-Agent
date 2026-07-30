from . import Any, Dict, OPTUNA_AVAILABLE, Path, json, logger, optuna
from ._omt_default_params import get_default_mcts_params_impl

def create_study_impl(study_name, storage, direction):
    if not OPTUNA_AVAILABLE:
        logger.error("Optuna is not available. Cannot create study.")
        return None
    return optuna.create_study(study_name=study_name, storage=storage, direction=direction, load_if_exists=True)

def save_best_params_impl(best_params_path, params):
    try:
        best_params_path.parent.mkdir(parents=True, exist_ok=True)
        best_params_path.write_text(json.dumps(params, indent=2), encoding="utf-8")
        logger.info(f"Saved best Optuna MCTS parameters to {best_params_path}")
    except Exception as e:
        logger.warning(f"Failed to save best Optuna MCTS parameters: {e}")

def load_best_params_impl(best_params_path):
    if best_params_path.exists():
        try: return json.loads(best_params_path.read_text(encoding="utf-8"))
        except Exception as e: logger.warning(f"Failed to load Optuna MCTS parameters from {best_params_path}: {e}")
    return get_default_mcts_params_impl()
