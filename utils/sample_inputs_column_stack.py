
def sample_inputs_column_stack(op_info, device, dtype, requires_grad, **kwargs):
    cases: tuple[tuple, tuple] = (  # type: ignore[assignment]
        ((S, 2, 1), (S, 3, 1)),
        ((S), (S, 5)), ((), (1, S))
    )
    make_tensor_partial = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    for shape1, shape2 in cases:
        yield SampleInput([make_tensor_partial(shape1), make_tensor_partial(shape2)])

