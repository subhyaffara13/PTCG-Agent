
def unwrap_peft_model(model):
    """
    Extract the base model from a PEFT-wrapped model.

    If the model is not a PEFT model, returns it unchanged. Otherwise, attempts to
    unwrap the base model using ``get_base_model()`` or the ``base_model.model`` attribute.

    Args:
        model: The model to unwrap.

    Returns:
        The unwrapped base model.

    Raises:
        AttributeError: If the model is a PEFT model but cannot be unwrapped safely.
    """
    if not _is_peft_model(model):
        return model
    if hasattr(model, "get_base_model"):
        return model.get_base_model()
    elif hasattr(model, "base_model") and hasattr(model.base_model, "model"):
        # PeftMixedModel do not provide a `get_base_model` method
        return model.base_model.model
    else:
        raise AttributeError("Cannot extract base model safely from this PEFT wrapper.")

