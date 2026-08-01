
def hp_params(trial):
    if is_optuna_available():
        import optuna

        if isinstance(trial, optuna.trial.BaseTrial):
            return trial.params

    if is_ray_tune_available():
        if isinstance(trial, dict):
            return trial

    if is_wandb_available():
        if isinstance(trial, dict):
            return trial

    raise RuntimeError(f"Unknown type for trial {trial.__class__}")

