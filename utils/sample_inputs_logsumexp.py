
def sample_inputs_logsumexp(self, device, dtype, requires_grad, **kwargs):
    inputs = (
        ((), (0,), True),
        ((S, S), (1,), True),
        ((S, S), (1,), False),
        ((S, S), (-2,), False),
        ((S, S), (0, 1), False),
    )
    # Test large inputs to check numerical stability
    lows = (None, 1e3, 1e6) if dtype in (torch.float32, torch.float64, torch.complex64, torch.complex128) else (None,)
    for low in lows:
        high = low * 2 if low is not None else None
        for shape, dim, keepdim in inputs:
            t = make_tensor(shape, dtype=dtype, device=device,
                            low=low, high=high,
                            requires_grad=requires_grad)
            yield SampleInput(t, dim, keepdim)

