
def error_inputs_huber_loss(op, device, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=torch.float32)
    # invalid reduction value
    err = 'is not a valid value for reduction'
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5, 4),), kwargs={'reduction': 'abc'}),
                     error_type=ValueError, error_regex=err)
    # delta <= 0
    for delta in (0, -1):
        err = 'huber_loss does not support non-positive values for delta.'
        yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5, 4),), kwargs={'delta': delta}),
                         error_type=RuntimeError, error_regex=err)

