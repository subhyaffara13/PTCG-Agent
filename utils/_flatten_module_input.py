
def _flatten_module_input(names, args, kwargs):
    """Flatten args and kwargs in a single tuple of tensors."""
    # extracted from https://github.com/microsoft/onnxruntime/blob/239c6ad3f021ff7cc2e6247eb074bd4208dc11e2/orttraining/orttraining/python/training/ortmodule/_io.py#L110

    def is_primitive_type(value):
        return type(value) in {int, bool, float}

    def to_tensor(value):
        return torch.tensor(value)

    ret = [to_tensor(arg) if is_primitive_type(arg) else arg for arg in args]
    ret += [
        to_tensor(kwargs[name]) if is_primitive_type(kwargs[name]) else kwargs[name] for name in names if name in kwargs
    ]

    # if kwargs is empty, append an empty dictionary at the end of the sample inputs to make exporter
    # happy. This is because the exporter is confused with kwargs and dictionary inputs otherwise.
    if not kwargs:
        ret.append({})

    return tuple(ret)

