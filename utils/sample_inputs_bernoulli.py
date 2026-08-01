
def sample_inputs_bernoulli(self, device, dtype, requires_grad, **kwargs):
    shapes = [
        [3],
        [],
        [0, 3],
        [2, 3, 4],
    ]

    for shape in shapes:
        t = make_tensor(shape, dtype=dtype, device=device,
                        low=0, high=1,
                        requires_grad=requires_grad)
        yield SampleInput(t)

