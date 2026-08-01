
def module_inputs_torch_nn_LeakyReLU(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((3, 2, 5)))),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input(4)),
                    reference_fn=no_batch_dim_reference_fn,
                    desc='no_batch_dim'),
        ModuleInput(constructor_input=FunctionInput(0.5),
                    forward_input=FunctionInput(make_input((3, 2, 5))),
                    desc='with_negval'),
        ModuleInput(constructor_input=FunctionInput(0.0),
                    forward_input=FunctionInput(make_input((10, 10))),
                    desc='with_zero_negval'),
        ModuleInput(constructor_input=FunctionInput(0.5),
                    forward_input=FunctionInput(make_input(())),
                    desc='with_negval_scalar')]

