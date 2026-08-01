
def _register_parameter_or_buffer(module, name, X) -> None:
    if isinstance(X, Parameter):
        module.register_parameter(name, X)
    else:
        module.register_buffer(name, X)

