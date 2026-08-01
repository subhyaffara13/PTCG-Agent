
def _generate_correlation_inputs(device, dtype, requires_grad, **kwargs):
    shapes = [(2,), (1, 2), (3, 2), (2, 3)]
    for shape in shapes:
        yield make_tensor(shape, dtype=dtype, device=device, requires_grad=requires_grad)

