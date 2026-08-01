
def sample_inputs_linalg_svdvals(op_info, device, dtype, requires_grad=False, **kwargs):
    make_arg = partial(
        make_tensor, dtype=dtype, device=device, requires_grad=requires_grad
    )

    batches = [(), (0,), (2,), (1, 1)]
    ns = [5, 2, 0]

    for batch, m, n in product(batches, ns, ns):
        yield SampleInput(make_arg(batch + (m, n)))

