
def sample_inputs_baddbmm(op_info, device, dtype, requires_grad, **kwargs):
    test_cases = [((S, S, M), (S, S, S), (S, S, M), 1, 1, False),
                  ((1,), (S, S, S), (S, S, M), 1, 1, True),
                  ((S, S, M), (S, S, S), (S, S, M), 0.6, 0.2, False),
                  ((1,), (S, S, S), (S, S, M), 0.6, 0.2, True),
                  ((), (S, S, S), (S, S, M), 1, 1, True),
                  ((), (S, S, S), (S, S, M), 0.6, 0.2, True),
                  ]
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad, low=None, high=None)
    for (input_shape, batch1_shape, batch2_shape, alpha, beta, broadcasts_input) in test_cases:
        yield SampleInput(
            make_arg(input_shape),
            make_arg(batch1_shape),
            make_arg(batch2_shape),
            beta=beta,
            alpha=alpha
        ).with_metadata(broadcasts_input=broadcasts_input)

        if dtype.is_complex:
            yield SampleInput(
                make_arg(input_shape),
                make_arg(batch1_shape),
                make_arg(batch2_shape),
                beta=beta * (1 + 2j),
                alpha=alpha * (2 + 3j),
            ).with_metadata(broadcasts_input=broadcasts_input)

    if dtype.is_complex:
        shapes = [(S, S, S), (S, M, S), (S, S, M)]
        args = tuple(make_arg(s) for s in shapes)
        yield SampleInput(
            args[0].transpose_(-1, 1),
            args[1].transpose(-1, 1).conj().requires_grad_(requires_grad),
            args[2].transpose(-1, 1).conj().requires_grad_(requires_grad),
            beta=beta * (1 + 2j),
            alpha=alpha * (2 + 3j),
        )

