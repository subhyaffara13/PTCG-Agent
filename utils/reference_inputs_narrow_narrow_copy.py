
def reference_inputs_narrow_narrow_copy(op_info, device, dtype, requires_grad, *, is_narrow, **kwargs):
    yield from sample_inputs_narrow_narrow_copy(op_info, device, dtype, requires_grad, is_narrow=is_narrow, **kwargs)

    shapes_and_args = (
        # 1-dim
        ((M,), 0, 0, 0),    # 0 elems from the left
        ((M,), -1, -1, 0),  # 0 elems from the right
        ((M,), 0, 5, 3),    # 3 elems from the left
        ((M,), 0, -5, 2),   # 2 elems from the right
        ((M,), -1, 0, M),   # M elems from the left
        ((M,), 0, -M, M),   # M elems from the right

        # 2-dim
        ((M, S), 1, 0, 0),    # dim 1, 0 elems from the left
        ((S, M), -2, -1, 0),  # dim 0, 0 elems from the right
        ((L, S), 1, 2, 3),    # dim 1, 3 elems from the left
        ((L, S), -1, 3, 2),   # dim 1, 2 elems from the left
        ((M, L), 0, 0, M),    # dim 0, M elems from the left
        ((M, L), -1, -L, L),  # dim 1, L elems from the right

        # 3-dim
        ((L, M, S), 2, 0, 0),    # dim 2, 0 elems from the left
        ((M, S, L), -1, -1, 0),  # dim 2, 0 elems from the right
        ((S, L, M), 2, 0, M),    # dim 2, M elems from the left
        ((L, S, M), -1, -M, M),  # dim 2, M elems from the right
        ((S, L, M), 1, 0, 0),    # dim 1, 0 elems from the left
        ((S, L, M), 0, 2, 1),    # dim 0, 1 elem from the left
        ((M, S, M), -1, -5, 4),  # dim 2, 4 elems from the right
    )

    for shape, dim, start, length in shapes_and_args:
        tensor = make_tensor(shape, dtype=dtype, device=device, low=None, high=None,
                             requires_grad=requires_grad)
        yield SampleInput(tensor, dim, start, length)
        # narrow also accepts the start argument being a Tensor
        if is_narrow:
            yield SampleInput(tensor, dim, torch.tensor(start), length)

