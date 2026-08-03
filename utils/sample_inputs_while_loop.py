import functools

def sample_inputs_while_loop(opinfo, device, dtype, requires_grad, **kwargs):
    make_arg = functools.partial(
        make_tensor, device=device, dtype=dtype, requires_grad=False
    )
    yield SampleInput(
        torch.tensor(3),
        make_arg(2, 3, 4, low=0.1, high=2),
    )

