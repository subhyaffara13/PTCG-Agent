
def module_inputs_torch_nn_CTCLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('blank', {'blank': 14})
    ]
    target_dtypes = [torch.int, torch.long]

    module_inputs = []
    for target_dtype, (desc, constructor_kwargs) in product(target_dtypes, cases):
        def reference_fn(m, p, i, t, il, tl, constructor_kwargs=constructor_kwargs):
            return ctcloss_reference(i, t, il, tl, **constructor_kwargs)

        blank = constructor_kwargs.get('blank', 0)
        low = 0 if blank == 14 else 1
        high = 14 if blank == 14 else 15

        module_inputs.append(
            ModuleInput(
                constructor_input=FunctionInput(**constructor_kwargs),
                forward_input=FunctionInput(make_input((50, 3, 15)).log_softmax(2),
                                            make_target((3, 30), dtype=target_dtype, low=low, high=high),
                                            (50, 50, 50), (30, 25, 20)),
                desc=f'{desc}_lengths_intlists',
                reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(
                constructor_input=FunctionInput(**constructor_kwargs),
                forward_input=FunctionInput(make_input((50, 3, 15)).log_softmax(2),
                                            make_target((3, 30), dtype=target_dtype, low=low, high=high),
                                            torch.tensor((50, 50, 50), device=device),
                                            torch.tensor((30, 25, 20), device=device)),
                desc=f'{desc}_lengths_tensors',
                reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(
                constructor_input=FunctionInput(**constructor_kwargs),
                forward_input=FunctionInput(make_input((50, 3, 15)).log_softmax(2),
                                            make_target((30 + 25 + 20,), dtype=target_dtype, low=low, high=high),
                                            (50, 50, 50), (30, 25, 20)),
                desc=f'{desc}_1d_target_lengths_intlists',
                reference_fn=reference_fn)
        )
        module_inputs.append(
            ModuleInput(
                constructor_input=FunctionInput(**constructor_kwargs),
                forward_input=FunctionInput(make_input((50, 3, 15)).log_softmax(2),
                                            make_target((30 + 25 + 20,), dtype=target_dtype, low=low, high=high),
                                            torch.tensor((50, 50, 50), device=device),
                                            torch.tensor((30, 25, 20), device=device)),
                desc=f'{desc}_1d_target_lengths_tensors',
                reference_fn=reference_fn)
        )

    return module_inputs

