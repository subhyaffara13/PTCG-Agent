
def module_error_inputs_torch_nn_MaxPool2d(module_info, device, dtype, requires_grad, training, **kwargs):
    """
    Error inputs for MaxPool2d that test error messages for invalid inputs.
    """
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        # Wrong input dimensions: 2D input instead of 3D/4D
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(2),
                forward_input=FunctionInput(make_input((3, 4))),  # 2D input
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex=r"non-empty 3D or 4D \(batch mode\) tensor expected for input"
        ),
        # Wrong input dimensions: 5D input
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(2),
                forward_input=FunctionInput(make_input((1, 2, 3, 4, 5))),  # 5D input
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex=r"non-empty 3D or 4D \(batch mode\) tensor expected for input"
        ),
        # Invalid padding: padding > kernel_size / 2
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(3, padding=5),  # kernel=3, pad=5 > 3/2
                forward_input=FunctionInput(make_input((1, 1, 10, 10))),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex=r"pad should be at most half of effective kernel size"
        ),
    ]

