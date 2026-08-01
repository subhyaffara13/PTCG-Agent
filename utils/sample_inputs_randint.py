
def sample_inputs_randint(self, device, dtype, requires_grad, **kwargs):
    low = 2
    high = 10

    for sample in sample_inputs_like_fns(self, device, dtype, requires_grad, **kwargs):
        sample.kwargs.setdefault('device', device)
        # With high
        yield SampleInput(high, sample.input.shape, *sample.args, **sample.kwargs)
        # With low and high
        yield SampleInput(low, high, sample.input.shape, *sample.args, **sample.kwargs)

