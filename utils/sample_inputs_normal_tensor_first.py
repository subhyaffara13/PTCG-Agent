
def sample_inputs_normal_tensor_first(self, device, dtype, requires_grad, **kwargs):
    # value_or_size, value_or_size, kwargs
    cases = [
        ([], [], {}),
        ([3], [3], {}),
        ([3, 4, 2], [3, 4, 2], {}),
        ([2, 3], 1.1, {}),
        ([1, 2, 3], [5, 2, 3], {}),  # broadcasting
    ]

    return sample_inputs_normal_common(self, device, dtype, requires_grad, cases, **kwargs)

