
def _check_forward_method(model):
    if not model._c._has_method("forward"):
        raise ValueError("input script module does not have forward method")

