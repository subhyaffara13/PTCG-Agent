
def sample_inputs_take(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    make_idx = partial(make_tensor, low=0, dtype=torch.int64, device=device, requires_grad=False)

    S = 3

    # Generic inputs: take S elements out of S * S
    index = make_idx((S,), high=(S * S))
    for idx in (index, -index - 1):
        yield SampleInput(input=make_arg((S, S)), args=(idx,))

    # Scalar cases
    scalar_sizes = [(), (1,)]
    src_gen = (make_arg(size) for size in scalar_sizes)
    idx_gen = (make_idx(size, high=1) for size in scalar_sizes)
    for src, idx in product(src_gen, idx_gen):
        yield SampleInput(input=src.clone().requires_grad_(requires_grad),
                          args=(idx.clone(),))

    # Empty cases
    src_sizes = [(0,), (), (1,), (3, 2)]
    src_gen = (make_arg(size) for size in src_sizes)

    idx = make_idx((0,), high=1)
    for src in src_gen:
        yield SampleInput(input=src.clone().requires_grad_(requires_grad),
                          args=(idx.clone(),))

