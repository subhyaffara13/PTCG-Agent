
def sample_inputs_tensordot(self, device, dtype, requires_grad, **kwargs):
    cases = (
        ((2, 2, 2), (2, 2, 2), (2)),
        ((2, 2, 1), (2, 1, 2), ([0, 1], [2, 0])),
        ((1, 1, 1), (2, 1, 2), ([0, 1], [2, 0])),
    )
    for first_shape, second_shape, dims in cases:
        yield SampleInput(make_tensor(first_shape, dtype=dtype, device=device,
                                      requires_grad=requires_grad, low=-1, high=+2),
                          make_tensor(second_shape, dtype=dtype, device=device,
                                      requires_grad=requires_grad, low=-1, high=+2),
                          dims=dims)

