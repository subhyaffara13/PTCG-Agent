import functools

def sample_inputs_local_map_hop(opinfo, device, dtype, requires_grad, **kwargs):
    # TODO: once HOPs support DTensor inputs, we should also test DTensors
    make_arg = functools.partial(
        make_tensor, device=device, dtype=dtype, requires_grad=False
    )
    yield SampleInput(
        make_arg(2, 3, 4, low=0.1, high=2),
        make_arg(2, 3, 4, low=0.1, high=2),
    )

