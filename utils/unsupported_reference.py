
def unsupported_reference(op_name):
    def _f(op, sample):
        raise RuntimeError(
            f"OpInfo for {op_name} does not define a ref() function. Support can be added by "
            "modifying torch/testing/_internal/opinfo/definitions/nested.py."
        )

    return _f

