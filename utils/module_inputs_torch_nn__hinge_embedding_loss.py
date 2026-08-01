
def module_inputs_torch_nn_HingeEmbeddingLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('margin', {'margin': 0.5})
    ]

    module_inputs = []
    for desc, constructor_kwargs in cases:
        def reference_fn(m, p, i, t, constructor_kwargs=constructor_kwargs):
            return hingeembeddingloss_reference(i, t, **constructor_kwargs)

        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input((10,)),
                                                    make_target((10,)).gt(0).to(dtype).mul_(2).sub_(1)),
                        desc=desc,
                        reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input(()),
                                                    make_target(()).gt(0).to(dtype).mul_(2).sub_(1)),
                        desc=f'scalar_{desc}',
                        reference_fn=reference_fn)
        )

    return module_inputs

