
def module_error_inputs_torch_nn_GroupNorm(module_info, device, dtype, requires_grad, training, **kwargs):
    """
    Error inputs for GroupNorm that test error messages include actual values.
    """
    return [
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(3, 10),  # num_groups=3, num_channels=10
                forward_input=FunctionInput(),  # Not needed for construction error
            ),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex=r"num_channels \(10\) must be divisible by num_groups \(3\)"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(5, 13),  # num_groups=5, num_channels=13
                forward_input=FunctionInput(),  # Not needed for construction error
            ),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex=r"num_channels \(13\) must be divisible by num_groups \(5\)"
        ),
    ]

