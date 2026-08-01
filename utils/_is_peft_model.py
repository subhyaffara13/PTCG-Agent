
def _is_peft_model(model):
    if is_peft_available():
        return isinstance(model, (PeftModel, PeftMixedModel))
    return False

