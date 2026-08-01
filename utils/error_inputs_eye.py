
def error_inputs_eye(op_info, device, **kwargs):
    # TODO: no layout
    _kwargs = {'device': device, 'dtype': torch.float32}

    yield ErrorInput(
        SampleInput(-1, args=(), kwargs=_kwargs),
        error_regex="n must be greater or equal to 0, got -1"
    )

    yield ErrorInput(
        SampleInput(-7, args=(42,), kwargs=_kwargs),
        error_regex="n must be greater or equal to 0, got -7"
    )

    yield ErrorInput(
        SampleInput(0, args=(-3,), kwargs=_kwargs),
        error_regex="m must be greater or equal to 0, got -3"
    )

