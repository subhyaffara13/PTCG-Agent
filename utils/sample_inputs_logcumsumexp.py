
def sample_inputs_logcumsumexp(self, device, dtype, requires_grad, **kwargs):
    inputs = (
        ((S, S, S), 0),
        ((S, S, S), 1),
        ((), 0),
    )

    for large_number in (True, False):
        for shape, dim in inputs:
            t = make_tensor(shape, dtype=dtype, device=device,
                            low=None, high=None,
                            requires_grad=requires_grad)

            if large_number and t.dim() > 0:
                t[0] = 10000
            yield SampleInput(t, dim)

