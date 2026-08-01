
def sample_inputs_empty_strided(op, device, dtype, requires_grad=False, **kwargs):

    inputs = [
        ((), (), {'dtype': dtype, 'device': device}),
        ((S,), (4,), {'dtype': dtype, 'device': device}),
        ((S, S), (2, 1), {'dtype': dtype, 'device': device}),
        ((S, S, S), (2, 0, 1), {'dtype': dtype, 'device': device}),
    ]

    for shape, strides, kwargs in inputs:
        yield SampleInput(shape, strides, requires_grad=requires_grad, **kwargs)

