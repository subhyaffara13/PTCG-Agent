
def _infer_pipeline_component(
    component,
    model_name,
    config,
    error_message,
    fallback_component=None,
):
    """Infer a component identifier from explicit input, then model/config fallbacks."""
    if component is not None:
        return component
    if isinstance(model_name, str):
        return model_name
    if isinstance(config, str):
        return config
    if fallback_component is not None:
        return fallback_component
    raise Exception(error_message)

