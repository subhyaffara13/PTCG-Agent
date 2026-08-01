
def sample_inputs_abs(op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs):
    yield from sample_inputs_elementwise_unary(op_info, device, dtype, requires_grad, op_kwargs=None, **kwargs)
    if dtype == torch.cfloat:
        yield SampleInput(torch.tensor(
            [
                1e-30 + 1e-30j,
                1e30 + 1e30j,
                1e-30 + 1e30j,
                1e30 + 1e-30j,
            ],
            device=device,
            dtype=dtype,
            requires_grad=requires_grad,
        ))

