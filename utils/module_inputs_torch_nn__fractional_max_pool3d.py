
def module_inputs_torch_nn_FractionalMaxPool3d(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_random_samples():
        return torch.empty((2, 4, 3), dtype=torch.double, device=device).uniform_()

    return [
        ModuleInput(
            constructor_input=FunctionInput(2, output_ratio=0.5, _random_samples=make_random_samples()),
            forward_input=FunctionInput(make_input((2, 4, 5, 5, 5))),
            desc='ratio'),
        ModuleInput(
            constructor_input=FunctionInput((2, 2, 2), output_size=(4, 4, 4), _random_samples=make_random_samples()),
            forward_input=FunctionInput(make_input((2, 4, 7, 7, 7))),
            desc='size'),
        ModuleInput(
            constructor_input=FunctionInput((4, 2, 3), output_size=(10, 3, 2), _random_samples=make_random_samples()),
            forward_input=FunctionInput(make_input((2, 4, 16, 7, 5))),
            desc='asymsize'),
        ModuleInput(
            constructor_input=FunctionInput(
                2, output_ratio=0.5, _random_samples=make_random_samples(), return_indices=True
            ),
            forward_input=FunctionInput(make_input((2, 4, 5, 5, 5))),
            desc='ratio_return_indices'),
        ModuleInput(
            constructor_input=FunctionInput(2, output_ratio=0.5, _random_samples=make_random_samples()),
            forward_input=FunctionInput(make_input((4, 5, 5, 5))),
            reference_fn=no_batch_dim_reference_fn,
            desc='ratio_no_batch_dim'),
        ModuleInput(
            constructor_input=FunctionInput((2, 2, 2), output_size=(4, 4, 4), _random_samples=make_random_samples()),
            forward_input=FunctionInput(make_input((4, 7, 7, 7))),
            reference_fn=no_batch_dim_reference_fn,
            desc='size_no_batch_dim'),
    ]

