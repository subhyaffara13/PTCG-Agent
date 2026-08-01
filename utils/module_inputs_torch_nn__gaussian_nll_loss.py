
def module_inputs_torch_nn_GaussianNLLLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('homoscedastic', {'homoscedastic': True}),
    ]

    module_inputs = []
    for desc, constructor_kwargs in cases:
        homoscedastic = constructor_kwargs.pop('homoscedastic', False)
        var_input = make_input(1, 3).abs() if homoscedastic else make_input(4, 1).abs()
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input(4, 3),
                                                    make_target(4, 3),
                                                    var_input),
                        desc=desc,
                        reference_fn=no_batch_dim_reference_fn)
        )

    return module_inputs

