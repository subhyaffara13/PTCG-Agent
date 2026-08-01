
def _generate_masked_op_mask(input_shape, device, **kwargs):
    make_arg = partial(
        make_tensor, dtype=torch.bool, device=device, requires_grad=False
    )
    yield None
    yield make_arg(input_shape)
    if len(input_shape) > 2:
        # broadcast last mask dimension:
        yield make_arg(input_shape[:-1] + (1,))
        # broadcast middle mask dimension:
        yield make_arg(input_shape[:1] + (1,) + input_shape[2:])
        # broadcast first mask dimension:
        yield make_arg((1,) + input_shape[1:])
        # mask.ndim < input.ndim
        yield make_arg(input_shape[1:])
        # mask.ndim == 1
        yield make_arg(input_shape[-1:])

