
def reference_inputs_margin_ranking_loss(op, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_margin_ranking_loss(op, device, dtype, requires_grad, **kwargs)
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    for reduction in ('sum', 'mean', 'none'):
        if dtype.is_floating_point:  # only supports ints and floats
            # NaN propagation
            inp1 = make_input((10, ))
            inp1[2] = float('nan')
            inp2 = make_input((10, ))
            inp2[4] = float('nan')
            target = make_input((10, ))
            inp2[9] = float('nan')
            yield SampleInput(inp1, args=(inp2, target), kwargs={'reduction': reduction})

            # Inf handling
            inp1 = make_input((10, ))
            inp2[1] = float('inf')
            inp2 = make_input((10, ))
            inp2[4] = float('inf')
            target = make_input((10, ))
            inp2[7] = float('inf')
            yield SampleInput(inp1, args=(inp2, target), kwargs={'reduction': reduction})

        # Broadcasting
        inp1 = make_input((5, 2))
        inp2 = make_input((5, 1))
        target = make_input((1, 2))
        yield SampleInput(inp1, args=(inp2, target), kwargs={'reduction': reduction})

