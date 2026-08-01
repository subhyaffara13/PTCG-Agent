
def sample_inputs_squeeze_multiple(op_info, device, dtype, requires_grad, **kwargs):
    shapes_and_args = (
        ((1, 1, 1, 1), ()),
        ((S, 1, S, 1), (1,)),
        ((S, 1, S, 1), (-1,)),
        ((S, 1, S, 1), (1, 3)),
        ((S, 1, S, 1), (1, 2,)),
        ((), (0,)),
    )

    for shape, dims in shapes_and_args:
        tensor = make_tensor(shape, dtype=dtype, device=device, low=None, high=None,
                             requires_grad=requires_grad)

        yield SampleInput(tensor, dims)

