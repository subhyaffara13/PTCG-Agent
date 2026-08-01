
def _generate_nan_reduction_inputs(device, dtype, requires_grad, **kwargs):
    yield from _generate_reduction_inputs(device, dtype, requires_grad)
    # NaN only exists for floating point numbers
    if dtype.is_complex or dtype.is_floating_point:
        yield torch.tensor([2, torch.nan, -1], device=device, dtype=dtype, requires_grad=requires_grad)
        yield torch.tensor([[torch.nan, 2], [0, 1]], device=device, dtype=dtype, requires_grad=requires_grad)

