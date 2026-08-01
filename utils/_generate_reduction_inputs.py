
def _generate_reduction_inputs(device, dtype, requires_grad, **kwargs):
    """Generates input tensors for testing reduction operators"""
    yield make_tensor([], dtype=dtype, device=device, requires_grad=requires_grad)
    yield make_tensor([2], dtype=dtype, device=device, requires_grad=requires_grad)
    yield make_tensor([3, 5], dtype=dtype, device=device, requires_grad=requires_grad)
    yield make_tensor(
        [3, 2, 1, 2], dtype=dtype, device=device, requires_grad=requires_grad
    )

