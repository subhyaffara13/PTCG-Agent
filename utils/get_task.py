
def get_task(model: str, token: str | None = None, **deprecated_kwargs) -> str:
    if is_offline_mode():
        raise RuntimeError("You cannot infer task automatically within `pipeline` when using offline mode")
    try:
        info = hf_api().model_info(model, token=token)
    except Exception as e:
        raise RuntimeError(f"Instantiating a pipeline without a task set raised an error: {e}")
    if not info.pipeline_tag:
        raise RuntimeError(
            f"The model {model} does not seem to have a correct `pipeline_tag` set to infer the task automatically"
        )
    if getattr(info, "library_name", "transformers") not in {"transformers", "timm"}:
        raise RuntimeError(f"This model is meant to be used with {info.library_name} not with transformers")
    task = info.pipeline_tag
    return task

