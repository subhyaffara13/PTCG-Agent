
def module_inputs_torch_nn_GroupNorm(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(
            constructor_input=FunctionInput(3, 6, 1e-3),
            forward_input=FunctionInput(make_input((4, 6, 5))),
            desc='1d_affine'),
        ModuleInput(
            constructor_input=FunctionInput(3, 6, 1e-3, bias=False),
            forward_input=FunctionInput(make_input((4, 6, 5))),
            desc='1d_affine_not_bias'),
        ModuleInput(
            constructor_input=FunctionInput(3, 12, 1e-3),
            forward_input=FunctionInput(make_input((4, 12))),
            desc='1d_affine_GN'),
        ModuleInput(
            constructor_input=FunctionInput(1, 6, 1e-3),
            forward_input=FunctionInput(make_input((150, 6))),
            desc='1d_affine_large_batch'),
        ModuleInput(
            constructor_input=FunctionInput(5, 5, 1e-3, False),
            forward_input=FunctionInput(make_input((4, 5, 5))),
            desc='1d_no_affine_IN'),
        ModuleInput(
            constructor_input=FunctionInput(1, 10, 1e-3, False),
            forward_input=FunctionInput(make_input((4, 10))),
            desc='1d_no_affine_LN'),
        ModuleInput(
            constructor_input=FunctionInput(3, 6, 1e-3),
            forward_input=FunctionInput(make_input((4, 6, 2, 3))),
            desc='2d_affine'),
        ModuleInput(
            constructor_input=FunctionInput(3, 9, 1e-3, bias=False),
            forward_input=FunctionInput(make_input((4, 9, 2, 3))),
            desc='2d_affine_not_bias'),
        ModuleInput(
            constructor_input=FunctionInput(3, 3, 1e-3, False),
            forward_input=FunctionInput(make_input((4, 3, 2, 3))),
            desc='2d_no_affine_IN'),
        ModuleInput(
            constructor_input=FunctionInput(1, 3, 1e-3, False),
            forward_input=FunctionInput(make_input((4, 3, 2, 3))),
            desc='2d_no_affine_LN'),]

