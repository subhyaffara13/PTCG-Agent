
def module_inputs_torch_nn_PReLU(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input(())),
                    desc='scalar'),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input(4)),
                    reference_fn=no_batch_dim_reference_fn,
                    desc='no_batch_dim'),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((2, 3, 4))),
                    reference_fn=lambda m, p, i: torch.clamp(i, min=0) + torch.clamp(i, max=0) * p[0][0],
                    desc='1d'),
        ModuleInput(constructor_input=FunctionInput(3),
                    forward_input=FunctionInput(make_input((2, 3, 4))),
                    reference_fn=lambda m, p, i: torch.clamp(i, min=0) + torch.clamp(i, max=0) * p[0][0],
                    desc='1d_multiparam'),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((2, 3, 4, 5))),
                    reference_fn=lambda m, p, i: torch.clamp(i, min=0) + torch.clamp(i, max=0) * p[0][0],
                    desc='2d'),
        ModuleInput(constructor_input=FunctionInput(3),
                    forward_input=FunctionInput(make_input((2, 3, 4, 5))),
                    reference_fn=lambda m, p, i: torch.clamp(i, min=0) + torch.clamp(i, max=0) * p[0][0],
                    desc='2d_multiparam'),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((2, 3, 4, 5, 6))),
                    reference_fn=lambda m, p, i: torch.clamp(i, min=0) + torch.clamp(i, max=0) * p[0][0],
                    desc='3d'),
        ModuleInput(constructor_input=FunctionInput(3),
                    forward_input=FunctionInput(make_input((2, 3, 4, 5, 6))),
                    reference_fn=lambda m, p, i: torch.clamp(i, min=0) + torch.clamp(i, max=0) * p[0][0],
                    desc='3d_multiparam')]

