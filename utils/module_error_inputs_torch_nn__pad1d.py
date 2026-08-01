
def module_error_inputs_torch_nn_Pad1d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    is_constant = kwargs.get('is_constant', False)

    return [
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(1, 3) if is_constant else FunctionInput(3),
                forward_input=FunctionInput(make_input((2, 3, 4, 5))),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=ValueError,
            error_regex=r"expected 2D or 3D input \(got 4D input\)",

        ),
    ]

