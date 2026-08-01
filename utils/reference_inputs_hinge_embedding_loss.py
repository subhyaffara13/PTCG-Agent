
def reference_inputs_hinge_embedding_loss(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_hinge_embedding_loss(op, device, dtype, requires_grad, **kwargs)
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    for reduction in ('sum', 'mean', 'none'):
        if dtype.is_floating_point:  # only supports ints and floats
            # NaN propagation
            inp = make_input((10, ))
            inp[2] = float('nan')
            target = make_input((10, ))
            # target should contain either 1 or -1 as per docs
            mask = torch.rand_like(target) > 0.5
            target[mask] = -1
            target[~mask] = 1
            yield SampleInput(inp, args=(target,), kwargs={'reduction': reduction})

            # Inf Handling
            inp = make_input((10, ))
            inp[4] = float('inf')
            target = make_input((10, ))
            mask = torch.rand_like(target) > 0.5
            target[mask] = -1
            target[~mask] = 1
            yield SampleInput(inp, args=(target,), kwargs={'reduction': reduction})

        # Broadcasting
        inp = make_input((5, 5))
        target = make_input((1, 5))
        mask = torch.rand_like(target) > 0.5
        target[mask] = -1
        target[~mask] = 1
        yield SampleInput(inp, args=(target,), kwargs={'reduction': reduction})

