
def sample_inputs_randint_like(self, device, dtype, requires_grad, **kwargs):
    low = 2
    high = 10

    for sample in sample_inputs_like_fns(self, device, dtype, requires_grad, **kwargs):
        # With high
        yield SampleInput(
            sample.input,
            high,
            *sample.args,
            **sample.kwargs)
        # With low and high
        yield SampleInput(
            get_independent_tensor(sample.input),
            low,
            high,
            *sample.args,
            **sample.kwargs)

