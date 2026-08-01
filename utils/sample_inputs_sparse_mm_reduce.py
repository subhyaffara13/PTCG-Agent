
def sample_inputs_sparse_mm_reduce(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    reductions = ["sum", "mean", "amax", "amin"]
    for m, k, reduce in product([5, 7], [3, 11], reductions):
        yield SampleInput(
            torch.eye(m, m)
            .to(device=device, dtype=dtype)
            .to_sparse_csr()
            .requires_grad_(requires_grad),
            make_arg((m, k)),
            reduce,
        )

