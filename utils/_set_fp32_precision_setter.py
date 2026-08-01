
def _set_fp32_precision_setter(backend, op):
    def inner(precision):
        return torch._C._set_fp32_precision_setter(backend, op, precision)

    return inner

