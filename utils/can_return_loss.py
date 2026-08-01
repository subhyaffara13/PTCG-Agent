
def can_return_loss(model_class):
    """
    Check if a given model can return loss.

    Args:
        model_class (`type`): The class of the model.
    """
    signature = inspect.signature(model_class.forward)

    for p in signature.parameters:
        if p == "return_loss" and signature.parameters[p].default is True:
            return True

    return False

