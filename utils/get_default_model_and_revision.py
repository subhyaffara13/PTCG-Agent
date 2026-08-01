
def get_default_model_and_revision(targeted_task: dict, task_options: Any | None) -> tuple[str, str]:
    """
    Select a default model to use for a given task.

    Args:
        targeted_task (`Dict`):
           Dictionary representing the given task, that should contain default models

        task_options (`Any`, None)
           Any further value required by the task to get fully specified.

    Returns

        Tuple:
            - `str` The model string representing the default model for this pipeline.
            - `str` The revision of the model.
    """
    defaults = targeted_task["default"]
    if task_options:
        if task_options not in defaults:
            raise ValueError(f"The task does not provide any default models for options {task_options}")
        default_models = defaults[task_options]["model"]
    elif "model" in defaults:
        default_models = targeted_task["default"]["model"]
    else:
        raise ValueError("The task defaults can't be correctly selected.")

    return default_models

