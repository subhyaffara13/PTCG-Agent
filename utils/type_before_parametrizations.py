
def type_before_parametrizations(module: Module) -> type:
    r"""Return the module type before parametrizations were applied and if not, then it returns the module type.

    Args:
        module (nn.Module): module to get type of
    """
    if is_parametrized(module):
        return module.__class__.__bases__[0]
    else:
        return type(module)

