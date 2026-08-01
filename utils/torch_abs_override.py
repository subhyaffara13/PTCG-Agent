
def torch_abs_override(input, *, out=None):
    if out is not None:
        raise AssertionError("Dont support in-place abs for MetaTensor analysis")
    return input

