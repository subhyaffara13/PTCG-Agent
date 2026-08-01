
def sample_inputs_cumprod(op_info, device, dtype, requires_grad, **kwargs):
    def make_arg(shape):
        # shrink values to be in the interval [-1, +1] for better precision in gradgradcheck
        return make_tensor(shape, dtype=dtype, device=device, low=-1, high=+1, requires_grad=requires_grad)

    def prod_zeros(dim_select):
        if len(dim_select) != 2:
            raise AssertionError(f"Expected len(dim_select) to be 2, got {len(dim_select)}")
        result = make_arg(3 * (S,))
        result.narrow(dim_select[0], 0, 1).narrow(dim_select[1], 1, 1).zero_()
        result.narrow(dim_select[0], 2, 1).narrow(dim_select[1], 3, 1).zero_()
        result.narrow(dim_select[0], 4, 1).narrow(dim_select[1], 3, 1).zero_()
        return result

    for dim in range(3):
        yield SampleInput(make_arg((S, S, S)), args=(dim,))
    # Scalar tensors and empty tensor
    for size in [(), (1,), (0,)]:
        yield SampleInput(make_arg(size), args=(0,))

    yield SampleInput(prod_zeros([0, 1]), args=(1,))
    yield SampleInput(prod_zeros([0, 2]), args=(1,))
    yield SampleInput(prod_zeros([1, 2]), args=(1,))

    # test dtype kwarg
    yield SampleInput(prod_zeros([1, 2]), args=(1,), kwargs={'dtype': dtype})

