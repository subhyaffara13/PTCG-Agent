
def module_inputs_torch_nn_GLU(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((5, 6)))),
        ModuleInput(constructor_input=FunctionInput(1),
                    forward_input=FunctionInput(make_input((5, 6, 7))),
                    desc='dim'),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((4,))),
                    desc='no_batch_dim',
                    reference_fn=no_batch_dim_reference_fn)]

