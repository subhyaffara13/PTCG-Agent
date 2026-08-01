
def sample_inputs_std_var(op_info, device, dtype, requires_grad, **kwargs):
    tensor_nd = partial(make_tensor, (S, S, S), device=device, dtype=dtype,
                        requires_grad=requires_grad)
    tensor_1d = partial(make_tensor, (S,), device=device, dtype=dtype,
                        requires_grad=requires_grad)

    yield SampleInput(tensor_nd())
    yield SampleInput(tensor_nd(), dim=1)
    yield SampleInput(tensor_nd(), dim=1, unbiased=True, keepdim=True)
    yield SampleInput(tensor_1d(), dim=0, unbiased=True, keepdim=True)
    yield SampleInput(tensor_1d(), dim=0, unbiased=False, keepdim=False)

    yield SampleInput(tensor_nd(), dim=(1,), correction=1.3)
    yield SampleInput(tensor_nd(), dim=(1,), correction=S // 2)
    yield SampleInput(tensor_nd(), dim=None, correction=0, keepdim=True)
    yield SampleInput(tensor_nd(), dim=None, correction=None)
    yield SampleInput(tensor_nd(), dim=None, correction=-1)
    yield SampleInput(tensor_nd(), dim=None, correction=-5)
    yield SampleInput(tensor_nd(), correction=0.5, keepdim=True)
    yield SampleInput(tensor_nd(), correction=0, keepdim=True)
    yield SampleInput(make_tensor(3, 4, 5, device=device, dtype=dtype, requires_grad=requires_grad), dim=-3)

