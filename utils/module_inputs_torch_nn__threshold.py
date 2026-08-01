
def module_inputs_torch_nn_Threshold(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(2., 1.),
                    forward_input=FunctionInput(make_input((2, 3, 4, 5))),
                    desc='threshold_value'),
        ModuleInput(constructor_input=FunctionInput(2., 10.),
                    forward_input=FunctionInput(make_input((2, 3, 4, 5))),
                    desc='large_value'),
        ModuleInput(constructor_input=FunctionInput(2., 1.),
                    forward_input=FunctionInput(make_input(())),
                    desc='threshold_value_scalar'),
        ModuleInput(constructor_input=FunctionInput(2., 1.),
                    forward_input=FunctionInput(make_input(4)),
                    reference_fn=no_batch_dim_reference_fn,
                    desc='no_batch_dim')]

