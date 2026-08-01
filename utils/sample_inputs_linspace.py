
def sample_inputs_linspace(op, device, dtype, requires_grad, **kwargs):
    ends = (-3, 0, 1, 4, 50)
    starts = (-2., 0, 4.3, 50)
    nsteps = (0, 1, 50)
    # Extra case to replicate off-by-one issue on CUDA
    cases = list(product(starts, ends, nsteps)) + [(0, 7, 50)]
    for start, end, nstep in cases:
        if dtype == torch.uint8 and (end < 0 or start < 0):
            continue
        yield SampleInput(start, args=(end, nstep), kwargs={"dtype": dtype, "device": device})

    yield SampleInput(1, args=(3, 1))

