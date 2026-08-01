
def sample_inputs_segment_reduce(op_info, device, dtype, requires_grad, *, mode='lengths', **kwargs):
    def _tensor(shape, dtype=dtype, low=None, high=None):
        return make_tensor(shape, dtype=dtype, device=device, low=low, high=high, requires_grad=requires_grad)

    test_cases = (
        # inp_shape, dim, lengths, unsafe
        ((S,), 0, [0, 1, 2, 2], False),
        ((S,), 0, [0, 1, 2, 2], True),
        ((S,), 0, [2, 0, 3, 0], False),
        ((S, S), 0, [0, 1, 2, 2], False),
        # test when lengths do not sum to dim size
        ((M, S, S), 0, [1, 2, 0, 6, 0], True),
        # test for higher dimensions
        ((S, S), 1, [[0, 1, 2, 2] for _ in range(S)], False),
        ((S, S), 1, [[2, 0, 3, 0], [0, 1, 2, 2], [3, 0, 2, 0], [1, 1, 1, 2], [0, 1, 2, 2]], False),
        ((S, S, S), 1, [[0, 1, 2, 2] for _ in range(S)], False),
        ((S, S, S), 1, [[2, 0, 3, 0], [0, 1, 2, 2], [3, 0, 2, 0], [1, 1, 1, 2], [0, 1, 2, 2]], False),
    )

    reductions = ["max", "mean", "min", "sum", "prod"]
    for args, reduce, initial in product(test_cases, reductions, [1, 2]):
        inp_shape, dim, lengths, unsafe = args
        lengths_t = torch.tensor(lengths, dtype=torch.long, device=device)
        sample_input_kwargs = {'axis': dim, 'unsafe': unsafe, 'initial': initial}
        if mode == 'lengths':
            sample_input_kwargs['lengths'] = lengths_t
        elif mode == 'offsets':
            zeros_shape = list(lengths_t.shape)
            zeros_shape[dim] = 1
            offsets_t = torch.cat((lengths_t.new_zeros(zeros_shape), lengths_t), dim).cumsum_(dim)
            sample_input_kwargs['offsets'] = offsets_t
        else:
            raise RuntimeError(f"mode most be one of 'offsets' or 'lengths' got '{mode}'.")
        yield SampleInput(_tensor(inp_shape),
                          args=(reduce,),
                          kwargs=sample_input_kwargs)

