
def _get_fp32_precision_getter(backend, op):
    def inner():
        return torch._C._get_fp32_precision_getter(backend, op)

    return inner

