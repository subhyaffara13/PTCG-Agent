
def error_inputs_multilabel_margin_loss(op, device, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=torch.float32)
    # invalid reduction
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(5, 4),), kwargs={'reduction': 'abc'}),
                     error_type=ValueError, error_regex='abc is not a valid value for reduction')
    # invalid input
    yield ErrorInput(SampleInput(make_input(5, 0), args=(make_input(5, 4),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'Expected non-empty vector or matrix with optional 0-dim batch size, but got: \[5, 0\]')
    yield ErrorInput(SampleInput(make_input(0,), args=(make_input(0,),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'Expected non-empty vector or matrix with optional 0-dim batch size, but got: \[0\]')
    # invalid target
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input(4,),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'inconsistent target size: \[4\] for input of size: \[5, 4\]')
    yield ErrorInput(SampleInput(make_input(5, 4), args=(make_input((),),), kwargs={}),
                     error_type=RuntimeError,
                     error_regex=r'inconsistent target size: \[\] for input of size: \[5, 4\]')

