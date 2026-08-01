
def sample_inputs_allclose(op_info, device, dtype, requires_grad, **kwargs):
    sample_shapes = [(), (S), (S, S, S)]
    atols = [1e-2, 1e-16]
    rtols = [1e-1, 0.5]
    for s, rtol, atol in product(sample_shapes, rtols, atols):
        # close sample
        t = make_tensor(s, device=device, dtype=dtype, requires_grad=requires_grad)
        close = (t + atol).detach().requires_grad_(requires_grad)
        yield SampleInput(t, close, rtol=rtol, atol=atol)

        # random sample
        a = make_tensor(s, device=device, dtype=dtype, requires_grad=requires_grad)
        b = make_tensor(s, device=device, dtype=dtype, requires_grad=requires_grad)
        yield SampleInput(a, b, rtol=rtol, atol=atol)

