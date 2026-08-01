
def get_name_by_module(model, module):
    """Get the name of a module within a model.

    Args:
        model: a model (nn.module) that equalization is to be applied on
        module: a module within the model

    Returns:
        name: the name of the module within the model
    """
    for name, m in model.named_modules():
        if m is module:
            return name
    raise ValueError("module is not in the model")

