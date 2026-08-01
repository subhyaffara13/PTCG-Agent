
def sample_inputs_multinomial(self, device, dtype, requires_grad, **kwargs):
    cases = [
        ([3], 3, {}),
        ([10], 3, {}),
        ([3, 10], 3, {}),
        ([3], 3, dict(replacement=False)),
        ([3], 3, dict(replacement=True)),
        ([3, 4], 4, dict(replacement=True)),
        ([3, 4], 4, dict(replacement=False)),
    ]

    for shape, num_samples, kwargs in cases:
        t = make_tensor(shape, dtype=dtype, device=device,
                        low=0, high=None,
                        requires_grad=requires_grad)
        yield SampleInput(t, num_samples, **kwargs)

