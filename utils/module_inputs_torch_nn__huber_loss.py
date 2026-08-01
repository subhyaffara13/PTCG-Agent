
def module_inputs_torch_nn_HuberLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
    ]

    module_inputs = []
    for desc, constructor_kwargs in cases:
        def reference_fn(m, p, i, t, constructor_kwargs=constructor_kwargs):
            return huberloss_reference(i, t, **constructor_kwargs)

        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input((5, 10)),
                                                    make_input((5, 10))),
                        desc=desc,
                        reference_fn=reference_fn)
        )

    return module_inputs

