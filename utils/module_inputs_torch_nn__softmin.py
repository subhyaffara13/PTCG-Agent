
def module_inputs_torch_nn_Softmin(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(1),
                    forward_input=FunctionInput(make_input((10, 20)))),
        ModuleInput(constructor_input=FunctionInput(1),
                    forward_input=FunctionInput(make_input((2, 3, 5, 10))),
                    desc='multidim'),
        ModuleInput(constructor_input=FunctionInput(0),
                    forward_input=FunctionInput(make_input(())),
                    desc='scalar'),
        ModuleInput(constructor_input=FunctionInput(-1),
                    forward_input=FunctionInput(make_input((3, 4, 10))),
                    reference_fn=no_batch_dim_reference_fn,
                    desc='no_batch_dim')]

