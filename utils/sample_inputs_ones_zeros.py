
def sample_inputs_ones_zeros(op, device, dtype, requires_grad, **kwargs):
    # this is a bit messy, as we want the args to be tuples
    # so if we pass size as a tuple, we have a tuple containing a tuple
    sizes = (
        (M,),
        (S, S),
    )
    for size in sizes:
        yield SampleInput(size, kwargs={'dtype': dtype, 'device': device})

