
def sample_inputs_linalg_matrix_norm(op_info, device, dtype, requires_grad, **kwargs):
    low_precision_dtypes = (torch.float16, torch.bfloat16, torch.complex32)
    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad
    )

    sizes = ((2, 2), (2, 3, 2))
    if dtype in low_precision_dtypes:
        # svdvals not supported for low precision dtypes
        ords = ("fro", inf, -inf, 1, -1)
    else:
        ords = ("fro", "nuc", inf, -inf, 1, -1, 2, -2)
    dims = ((-2, -1), (-1, 0))

    for size, ord, dim, keepdim in product(sizes, ords, dims, [True, False]):
        yield SampleInput(make_arg(size), args=(ord, dim, keepdim))

