
def _filter_model_params(model_params: dict) -> dict:
    """Remove 'messages' param from model params."""
    return {k: v for k, v in model_params.items() if k != "messages"}

