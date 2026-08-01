
def module_inputs_torch_nn_MultiMarginLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=torch.long, requires_grad=False)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('p', {'p': 2}),
        ('margin', {'margin': 0.5}),
        ('weights', {'weight': make_weight(10)})
    ]

    module_inputs = []
    for desc, constructor_kwargs in cases:
        def reference_fn(m, p, i, t, constructor_kwargs=constructor_kwargs):
            return multimarginloss_reference(i, t, **constructor_kwargs)

        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input((5, 10)),
                                                    make_target((5), low=0, high=10)),
                        desc=desc,
                        reference_fn=reference_fn)
        )

    return module_inputs

