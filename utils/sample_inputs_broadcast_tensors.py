
def sample_inputs_broadcast_tensors(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    test_cases: tuple[tuple] = (((3,), (1, 2, 1), (1, 1), (5, 1, 1),),)

    for shape, *other_shapes in test_cases:
        yield SampleInput(make_arg(shape), args=tuple(make_arg(s) for s in other_shapes))

