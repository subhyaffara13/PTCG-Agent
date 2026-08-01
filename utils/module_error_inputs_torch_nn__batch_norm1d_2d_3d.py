
def module_error_inputs_torch_nn_BatchNorm1d_2d_3d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    if module_info.module_cls == torch.nn.BatchNorm1d:
        input_shape = (2, 10)
    elif module_info.module_cls == torch.nn.BatchNorm2d:
        input_shape = (2, 10, 5, 5)
    else:
        input_shape = (2, 10, 4, 4, 4)

    return [
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, eps=-1.0),
                forward_input=FunctionInput(make_input(input_shape)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=ValueError,
            error_regex="eps must be positive"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, eps=0.0),
                forward_input=FunctionInput(make_input(input_shape)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=ValueError,
            error_regex="eps must be positive"
        ),
    ]

