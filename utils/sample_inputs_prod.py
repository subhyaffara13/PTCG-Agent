
def sample_inputs_prod(op_info, device, dtype, requires_grad, **kwargs):
    def make_arg(shape):
        # shrink values to be in the interval [-1, +1] for better precision in gradgradcheck
        return make_tensor(shape, dtype=dtype, device=device, low=-1, high=+1, requires_grad=requires_grad)

    def prod_single_zero():
        result = make_arg(2 * (S,))
        result[0, 1] = 0
        return result

    for sample in sample_inputs_cumprod(op_info, device, dtype, requires_grad):
        # only Tensor, ignore other inputs
        yield SampleInput(sample.input.clone().requires_grad_(requires_grad))
        yield sample

    # Generates samples with keepdim = True
    for sample in sample_inputs_cumprod(op_info, device, dtype, requires_grad):
        sample.kwargs['keepdim'] = True
        yield sample

    yield SampleInput(prod_single_zero())
    yield SampleInput(make_arg((3, 3, 3)), args=(1,))
    yield SampleInput(make_arg((3, 3, 3)), args=(1,), kwargs={'keepdim': True})

    yield SampleInput(make_arg((3, 0)), args=(1,))
    yield SampleInput(make_arg((3, 0)), args=(1,), kwargs={'keepdim': True})
    yield SampleInput(torch.tensor([2., 3, 0, 0], dtype=dtype, device=device, requires_grad=requires_grad))

    # test zero scalar tensor
    zero = make_arg(())
    zero.zero_()
    yield SampleInput(zero.clone().requires_grad_(requires_grad))
    yield SampleInput(zero.clone().requires_grad_(requires_grad), args=(0,))
    yield SampleInput(zero.clone().requires_grad_(requires_grad),
                      args=(0,),
                      kwargs={'keepdim': True})

