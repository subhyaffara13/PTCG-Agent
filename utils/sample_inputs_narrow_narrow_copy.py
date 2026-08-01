
def sample_inputs_narrow_narrow_copy(op_info, device, dtype, requires_grad, *, is_narrow, **kwargs):
    shapes_and_args = (
        ((S, S, S), 1, 2, 2),
        ((S, S, S), -1, 2, 2),
        ((S, S, S), 1, 0, 0),
        ((S, S, S), -1, 0, 0),
        ((S, S, S), 2, 1, 2),
    )

    for shape, dim, start, length in shapes_and_args:
        tensor = make_tensor(shape, dtype=dtype, device=device, low=None, high=None,
                             requires_grad=requires_grad)
        yield SampleInput(tensor, dim, start, length)
        # narrow also accepts the start argument being a Tensor
        if is_narrow:
            yield SampleInput(tensor, dim, torch.tensor(start), length)

