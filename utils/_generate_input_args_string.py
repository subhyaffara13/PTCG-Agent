
def _generate_input_args_string(obj):
    """Generate a string for the input arguments of an object."""
    signature = inspect.signature(obj.__class__)
    input_param_names = set(signature.parameters.keys())
    result = []
    for name, value in inspect.getmembers(obj):
        if name in input_param_names:
            result.append((name, _simplify_obj_name(value)))
    return ", ".join([f"{name}={value}" for name, value in result])

