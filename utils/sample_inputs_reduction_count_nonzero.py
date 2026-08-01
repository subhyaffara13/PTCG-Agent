
def sample_inputs_reduction_count_nonzero(*args, **kwargs):
    """Sample inputs for count_nonzero"""
    # count_nonzero does not support keepdim yet
    for sample in sample_inputs_reduction(*args, **kwargs):
        sample.kwargs.pop('keepdim', None)
        yield sample

