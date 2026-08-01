
def sample_inputs_normal_common(self, device, dtype, requires_grad, cases, **kwargs):
    def get_value_or_make_tensor(value_or_shape):
        if isinstance(value_or_shape, list):
            return make_tensor(value_or_shape, dtype=dtype, device=device,
                               low=0, high=None,
                               requires_grad=requires_grad)
        return value_or_shape

    for value_or_mean_shape, value_or_std_shape, kwargs in cases:
        mean = get_value_or_make_tensor(value_or_mean_shape)
        std = get_value_or_make_tensor(value_or_std_shape)
        yield SampleInput(mean, std, **kwargs)

