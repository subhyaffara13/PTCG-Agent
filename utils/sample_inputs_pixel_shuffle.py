
def sample_inputs_pixel_shuffle(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    yield from (
        SampleInput(make_arg((1, 9, 2, 2)), upscale_factor=upscale_factor)
        for upscale_factor in (1, 3)
    )
    yield from (
        SampleInput(make_arg(shape), upscale_factor=1)
        for shape in [
            (1, 0, 1, 1),
            (1, 1, 0, 1),
            (1, 1, 1, 0),
        ]
    )

