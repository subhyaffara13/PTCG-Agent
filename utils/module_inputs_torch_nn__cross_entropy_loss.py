
def module_inputs_torch_nn_CrossEntropyLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=torch.long, requires_grad=False)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    reductions: list[str] = ['mean', 'sum', 'none']
    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('weights', {'weight': make_weight((3,))}),
        ('ignore_index', {'ignore_index': 1}),
        ('label_smoothing', {'label_smoothing': 0.15}),
        ('ignore_index_label_smoothing', {'ignore_index': 1, 'label_smoothing': 0.15})
    ]

    module_inputs = []
    for reduction, (desc, constructor_kwargs) in product(reductions, cases):
        def reference_fn(m, p, i, t, reduction=reduction, constructor_kwargs=constructor_kwargs):
            return cross_entropy_loss_reference(i, t, reduction=reduction, **constructor_kwargs)

        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                        forward_input=FunctionInput(make_input((2, 3, 5, 5)),
                                                    make_target((2, 5, 5), low=0, high=3)),
                        desc=f"4d_{desc}_{reduction}",
                        reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                        forward_input=FunctionInput(make_input((2, 3, 5)),
                                                    make_target((2, 5), low=0, high=3)),
                        desc=f"3d_{desc}_{reduction}",
                        reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                        forward_input=FunctionInput(make_input((2, 3)),
                                                    make_target((2), low=0, high=3)),
                        desc=f"2d_{desc}_{reduction}",
                        reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                        forward_input=FunctionInput(make_input((2, 3, 5, 5, 2, 2)),
                                                    make_target((2, 5, 5, 2, 2), low=0, high=3)),
                        desc=f"higher_dim_{desc}_{reduction}",
                        reference_fn=reference_fn)
        )

        if constructor_kwargs.get('ignore_index', None) is None:
            module_inputs.append(
                ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                            forward_input=FunctionInput(make_input((5, 3, 4, 2)),
                                                        make_input((5, 3, 4, 2)).softmax(dim=1)),
                            desc=f"4d_prob_target_{desc}_{reduction}",
                            reference_fn=reference_fn)
            )
            module_inputs.append(
                ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                            forward_input=FunctionInput(make_input((5, 3, 4)),
                                                        make_input((5, 3, 4)).softmax(dim=1)),
                            desc=f"3d_prob_target_{desc}_{reduction}",
                            reference_fn=reference_fn)
            )
            module_inputs.append(
                ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                            forward_input=FunctionInput(make_input((5, 3)),
                                                        make_input((5, 3)).softmax(dim=1)),
                            desc=f"2d_prob_target_{desc}_{reduction}",
                            reference_fn=reference_fn)
            )
            module_inputs.append(
                ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                            forward_input=FunctionInput(make_input((2, 3, 5, 5, 2, 2)),
                                                        make_input((2, 3, 5, 5, 2, 2)).softmax(dim=1)),
                            desc=f"higher_dim_prob_target_{desc}_{reduction}",
                            reference_fn=reference_fn)
            )
            module_inputs.append(
                ModuleInput(constructor_input=FunctionInput(reduction=reduction, **constructor_kwargs),
                            forward_input=FunctionInput(make_input((3,)),
                                                        make_target((), low=0, high=3)),
                            desc=f"no_batch_dim_{desc}_{reduction}",
                            reference_fn=partial(no_batch_dim_reference_fn, is_criterion=True))
            )

    return module_inputs

