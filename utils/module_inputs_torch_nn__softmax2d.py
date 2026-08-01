
def module_inputs_torch_nn_Softmax2d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((1, 3, 10, 20))),
                    reference_fn=lambda m, p, i: torch.exp(i).div(torch.exp(i).sum(1, False))),
        ModuleInput(constructor_input=FunctionInput(),
                    forward_input=FunctionInput(make_input((3, 4, 5))),
                    reference_fn=no_batch_dim_reference_fn,
                    desc='no_batch_dim')]

