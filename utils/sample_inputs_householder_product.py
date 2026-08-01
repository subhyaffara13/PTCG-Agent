
def sample_inputs_householder_product(op_info, device, dtype, requires_grad, **kwargs):
    """
    This function generates input for torch.linalg.householder_product (torch.orgqr).
    The first argument should be a square matrix or batch of square matrices, the second argument is a vector or batch of vectors.
    Empty, square, rectangular, batched square and batched rectangular input is generated.
    """
    make_arg = partial(
        make_tensor,
        device=device,
        dtype=dtype,
        requires_grad=requires_grad,
        low=-2,
        high=2,
    )
    # Each column of the matrix is getting multiplied many times leading to very large values for
    # the Jacobian matrix entries and making the finite-difference result of grad check less accurate.
    # That's why gradcheck with the default range [-9, 9] fails and [-2, 2] is used here.
    yield SampleInput(make_arg((S, S)), make_arg((S,)))
    yield SampleInput(make_arg((S + 1, S)), make_arg((S,)))
    yield SampleInput(make_arg((2, 1, S, S)), make_arg((2, 1, S)))
    yield SampleInput(make_arg((2, 1, S + 1, S)), make_arg((2, 1, S)))
    yield SampleInput(
        make_arg((0, 0), low=None, high=None),
        make_arg((0,), low=None, high=None),
    )
    yield SampleInput(make_arg((S, S)), make_arg((0,), low=None, high=None))
    # m = n = S, k = S - 2
    yield SampleInput(make_arg((S, S)), make_arg((S - 2,), low=None, high=None))
    # m = S, n = S -1, k = S - 2
    yield SampleInput(make_arg((S, S - 1)), make_arg((S - 2,), low=None, high=None))

