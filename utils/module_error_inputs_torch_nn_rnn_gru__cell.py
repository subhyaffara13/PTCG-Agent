
def module_error_inputs_torch_nn_RNN_GRU_Cell(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    samples = [
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, 20),
                forward_input=FunctionInput(make_input(3, 11), make_input(3, 20)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="input has inconsistent input_size: got 11 expected 10"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, 20),
                forward_input=FunctionInput(make_input(3, 10), make_input(3, 21)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="hidden0 has inconsistent hidden_size: got 21, expected 20"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, 20),
                forward_input=FunctionInput(make_input(3, 10), make_input(5, 20)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="Input batch size 3 doesn't match hidden0 batch size 5"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, 20),
                forward_input=FunctionInput(make_input(3, 10), make_input(3, 1, 1, 20)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=ValueError,
            error_regex="Expected hidden to be 1D or 2D, got 4D instead"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, 20, 'relu'),
                forward_input=FunctionInput(make_input(3, 10), make_input(3, 21)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="hidden0 has inconsistent hidden_size: got 21, expected 20"
        ),
        ErrorModuleInput(
            ModuleInput(
                constructor_input=FunctionInput(10, 20, 'tanh'),
                forward_input=FunctionInput(make_input(3, 10), make_input(3, 21)),
            ),
            error_on=ModuleErrorEnum.FORWARD_ERROR,
            error_type=RuntimeError,
            error_regex="hidden0 has inconsistent hidden_size: got 21, expected 20"
        ),
    ]
    return samples

