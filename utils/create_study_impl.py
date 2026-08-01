
def create_study_impl(study_name, storage, direction):
    if not OPTUNA_AVAILABLE:
        logger.error("Optuna is not available. Cannot create study.")
        return None
    return optuna.create_study(study_name=study_name, storage=storage, direction=direction, load_if_exists=True)

