
def sample_inputs_linalg_pinv_singular(
    op_info, device, dtype, requires_grad=False, **kwargs
):
    """
    This function produces factors `a` and `b` to generate inputs of the form `a @ b.t()` to
    test the backward method of `linalg_pinv`. That way we always preserve the rank of the
    input no matter the perturbations applied to it by the gradcheck.
    Note that `pinv` is Frechet-differentiable in a rank-preserving neighborhood.
    """
    batches = [(), (0,), (2,), (1, 1)]
    # the size of at least 30 is required to cause failures for the previous implicit implementation
    # of the pinv's backward method, albeit it is slow.
    size = [0, 3, 50]

    for batch, m, n in product(batches, size, size):
        for k in range(min(3, m, n)):
            # Note that by making the columns of `a` and `b` orthonormal we make sure that
            # the product matrix `a @ b.t()` has condition number 1 when restricted to its image
            a = (
                torch.rand(*batch, m, k, device=device, dtype=dtype)
                .qr()
                .Q.requires_grad_(requires_grad)
            )
            b = (
                torch.rand(*batch, n, k, device=device, dtype=dtype)
                .qr()
                .Q.requires_grad_(requires_grad)
            )
            yield SampleInput(a, args=(b,))

