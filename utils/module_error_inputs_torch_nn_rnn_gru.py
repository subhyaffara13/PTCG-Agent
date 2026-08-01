
def module_error_inputs_torch_nn_RNN_GRU(module_info, device, dtype, requires_grad, training, **kwargs):
    # use float64 for dtype mismatch test if current dtype is float32, otherwise use float32
    # MPS doesn't support float64, so use float16 instead
    # Extract device type from device string (e.g., 'mps:0' -> 'mps')
    device_type = device.split(':')[0] if isinstance(device, str) else device.type
    if dtype == torch.float32:
        mismatched_dtype = torch.float16 if device_type == 'mps' else torch.float64
    else:
        mismatched_dtype = torch.float32
    make_input = partial(make_tensor, device=device, dtype=mismatched_dtype, requires_grad=requires_grad)

    samples = [
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(10, 0, 1)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex="hidden_size must be greater than zero"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(10, 10, 0)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex="num_layers must be greater than zero"
        ),
        # Test dtype mismatch error message
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(3, 5, dtype=dtype, device=device),
                forward_input=FunctionInput(make_input((2, 4, 3))),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=ValueError,
            error_regex=(r"RNN input dtype .* does not match weight dtype .* "
                         r"Convert input: input\.to\(.*\), or convert model: model\.to\(.*\)")
        ),
        # Test bias parameter type validation
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5, bias=0)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="bias should be of type bool, got: int"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5, bias=1)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="bias should be of type bool, got: int"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5, bias="True")),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="bias should be of type bool, got: str"
        ),
        # Test batch_first parameter type validation
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5, batch_first=0)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="batch_first should be of type bool, got: int"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5, batch_first=1)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="batch_first should be of type bool, got: int"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5, batch_first="False")),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="batch_first should be of type bool, got: str"
        ),
        # Test input_size parameter type validation
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3.0, 5)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="input_size should be of type int, got: float"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput("10", 5)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="input_size should be of type int, got: str"
        ),
        # Test input_size parameter value validation
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(0, 5)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex="input_size must be greater than zero"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(-1, 5)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex="input_size must be greater than zero"
        ),
        # Test hidden_size parameter type validation
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(3, 5.0)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=TypeError,
            error_regex="hidden_size should be of type int, got: float"
        ),
    ]
    return samples

