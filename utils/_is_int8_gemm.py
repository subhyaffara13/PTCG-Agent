
def _is_int8_gemm(inputs):
    return (
        isinstance(inputs[0], ir.IRNode)
        and inputs[0].get_dtype() in [torch.uint8, torch.int8]
    ) or (
        isinstance(inputs[0], torch.Tensor)
        and inputs[0].dtype in [torch.uint8, torch.int8]
    )

