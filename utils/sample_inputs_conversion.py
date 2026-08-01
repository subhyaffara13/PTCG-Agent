
def sample_inputs_conversion(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    shapes = ((),
              (2, 3))
    memory_format_options = [None, torch.contiguous_format]

    for shape, memory_format in itertools.product(shapes, memory_format_options):
        yield SampleInput(make_arg(shape),
                          kwargs={'memory_format': memory_format} if memory_format else {})
    yield SampleInput(make_arg((2, 3, 2, 3)), kwargs={'memory_format': torch.channels_last})

