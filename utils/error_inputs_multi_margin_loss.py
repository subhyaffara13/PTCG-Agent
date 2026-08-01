
def error_inputs_multi_margin_loss(op, device, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=torch.float32)
    # invalid reduction
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5,),), kwargs={'reduction': 'abc'}),
                     error_type=ValueError, error_regex='abc is not a valid value for reduction')
    # invalid input
    yield ErrorInput(SampleInput(make_input(5, 0), args=(make_input(5,),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'Expected non-empty vector or matrix with optional 0-dim batch size, but got: \[5, 0\]')
    yield ErrorInput(SampleInput(make_input(0,), args=(make_input(5,),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'Expected non-empty vector or matrix with optional 0-dim batch size, but got: \[0\]')
    # invalid target
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5, 4),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'target tensor should be 1-D with size equal to.*Expected target size \[5\].*but got \[5, 4\]')
    # invalid target dtype
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5,),), kwargs={}),
                     error_type=RuntimeError, error_regex='expected scalar type Long but found Float')
    # invalid weight
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5,),), kwargs={'weight': make_input(())}),
                     error_type=ValueError, error_regex='weight must be one-dimensional')
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5,),), kwargs={'weight': make_input(5, 4)}),
                     error_type=ValueError, error_regex='weight must be one-dimensional')
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5,),), kwargs={'weight': make_input(5,)}),
                     error_type=RuntimeError, error_regex=r'inconsistent weight size, expected 4 but got \[5\]')
    # invalid p
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5,),), kwargs={'p': 3}),
                     error_type=ValueError, error_regex='only p == 1 and p == 2 supported')

