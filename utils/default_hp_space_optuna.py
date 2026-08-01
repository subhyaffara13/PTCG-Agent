
def default_hp_space_optuna(trial) -> dict[str, float]:
    from .integrations import is_optuna_available

    if not is_optuna_available():
        raise ImportError("This function needs Optuna installed: `pip install optuna`")
    return {
        "learning_rate": trial.suggest_float("learning_rate", 1e-6, 1e-4, log=True),
        "num_train_epochs": trial.suggest_int("num_train_epochs", 1, 5),
        "seed": trial.suggest_int("seed", 1, 40),
        "per_device_train_batch_size": trial.suggest_categorical("per_device_train_batch_size", [4, 8, 16, 32, 64]),
    }

