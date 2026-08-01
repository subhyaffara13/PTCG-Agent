
def unsupported_sample_inputs_func(op_name):
    def _f(op_info, device, dtype, requires_grad, op_name=op_name, **kwargs):
        raise RuntimeError(
            f"OpInfo for {op_name} does not support NJT. Support can be added by modifying "
            "torch/testing/_internal/opinfo/definitions/nested.py."
        )

    return _f

