
def error_inputs_arange(op, device, **kwargs):
    yield ErrorInput(SampleInput(0, args=(3, 0)), error_type=RuntimeError, error_regex='step must be nonzero')
    yield ErrorInput(SampleInput(0, args=(-3, 2)), error_type=RuntimeError,
                     error_regex='upper bound and lower bound inconsistent with step sign')
    yield ErrorInput(SampleInput(0, args=(3, -2)), error_type=RuntimeError,
                     error_regex='upper bound and lower bound inconsistent with step sign')
    yield ErrorInput(SampleInput(1549556900, args=(1549556828, 1989724)), error_type=RuntimeError,
                     error_regex='upper bound and lower bound inconsistent with step sign')
    yield ErrorInput(SampleInput(0, args=(float('inf'), 2)), error_type=RuntimeError, error_regex='unsupported range')
    yield ErrorInput(SampleInput(float('-inf'), args=(1, 2)), error_type=RuntimeError, error_regex='unsupported range')

