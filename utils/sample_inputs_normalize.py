
def sample_inputs_normalize(self, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, low=-1, high=1, device=device, dtype=dtype, requires_grad=requires_grad)

    cases: tuple[tuple[int, ...], dict] = (
        ((2, 1, 4, 5), {'p': 1., 'dim': 2}),
        ((2, 3, 4, 5), {'p': 2., 'dim': 1}),
        ((1, 2, 4, 5), {'p': 0.5, 'dim': 0}),
        ((1, 3, 4, 5), {'p': -1., 'dim': 1}),
        ((1, 3, 4, 5), {'p': 0., 'dim': -1}),
        ((), {'p': 1.2, 'dim': 0}),
        ((2, 3, 4, 5), {}),
        ((2, 3, 4, 5), {'eps': 1e-4}))

    for input_shape, kwargs in cases:
        yield SampleInput(make_arg(input_shape), kwargs=kwargs)

