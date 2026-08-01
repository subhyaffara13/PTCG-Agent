
def _remove_none_from_inputs(model_args):
    return tuple(arg for arg in model_args if arg is not None)

