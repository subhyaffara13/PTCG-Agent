
def module_inputs_torch_nn_BCELoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('weights', {'weight': make_weight((10,))}),
    ]

    def bce_loss_reference_fn(m, p, i, t, reduction='mean', weight=None):
        result = -(t * i.log() + (1 - t) * (1 - i).log())

        if weight is not None:
            result = result * weight

        if reduction == 'none':
            return result
        elif reduction == 'mean':
            return result.sum() / i.numel()
        else:
            return result.sum()

    module_inputs = []
    for desc, constructor_kwargs in cases:
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input((15, 10), low=1e-2, high=1 - 1e-2),
                                                    make_target((15, 10)).gt(0).to(dtype)),
                        desc=desc,
                        reference_fn=partial(bce_loss_reference_fn, **constructor_kwargs))
        )

    scalar_weight = make_weight(())
    module_inputs.append(
        ModuleInput(constructor_input=FunctionInput(weight=scalar_weight),
                    forward_input=FunctionInput(make_input((), low=1e-2, high=1 - 1e-2),
                                                make_target(()).gt(0).to(dtype)),
                    desc='scalar_weight',
                    reference_fn=partial(bce_loss_reference_fn, weight=scalar_weight))
    )

    return module_inputs

