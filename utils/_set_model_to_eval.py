
def _set_model_to_eval(model):
    """Context manager to temporarily set the training mode of ``model`` to eval."""
    if not isinstance(model, torch.jit.ScriptFunction):
        originally_training = model.training
        model.train(False)
        try:
            yield
        finally:
            model.train(originally_training)
    else:
        # Do nothing for ScriptFunction
        try:
            yield
        finally:
            pass

