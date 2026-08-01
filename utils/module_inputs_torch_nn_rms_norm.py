
def module_inputs_torch_nn_RMSNorm(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def rms_norm_reference_fn(m, p, i):
        eps = m.eps
        if eps is None:
            eps = torch.finfo(i.dtype).eps
        ndim = i.ndim
        normalized_shape = m.normalized_shape
        weight = m.weight
        dims = [ndim - i - 1 for i in range(len(normalized_shape))]
        upcasted_i = i.float()
        result = upcasted_i * torch.rsqrt(upcasted_i.pow(2).mean(dim=dims, keepdim=True) + m.eps)
        if weight is not None:
            result *= weight
        return result.type_as(i)

    return [
        ModuleInput(
            constructor_input=FunctionInput([5], 1e-3),
            forward_input=FunctionInput(make_input((4, 5, 5))),
            desc='1d_elementwise_affine',
            reference_fn=rms_norm_reference_fn),
        ModuleInput(
            constructor_input=FunctionInput([5], 1e-3),
            forward_input=FunctionInput(make_input((128, 5, 5))),
            desc='1d_elementwise_affine_large_batch',
            reference_fn=rms_norm_reference_fn),
        ModuleInput(
            constructor_input=FunctionInput([5], 1e-3, False),
            forward_input=FunctionInput(make_input((4, 5, 5))),
            desc='1d_no_elementwise_affine',
            reference_fn=rms_norm_reference_fn),
        ModuleInput(
            constructor_input=FunctionInput([2, 2, 5], 1e-3),
            forward_input=FunctionInput(make_input((4, 2, 2, 5))),
            desc='3d_elementwise_affine',
            reference_fn=rms_norm_reference_fn),
        ModuleInput(
            constructor_input=FunctionInput([2, 2, 5], 1e-3, False),
            forward_input=FunctionInput(make_input((4, 2, 2, 5))),
            desc='3d_no_elementwise_affine',
            reference_fn=rms_norm_reference_fn),
        ModuleInput(
            constructor_input=FunctionInput([5], 1e-3),
            forward_input=FunctionInput(make_input((0, 5))),
            desc='1d_empty_elementwise_affine',
            reference_fn=rms_norm_reference_fn),
    ]

