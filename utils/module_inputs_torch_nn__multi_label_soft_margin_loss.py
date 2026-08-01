
def module_inputs_torch_nn_MultiLabelSoftMarginLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=torch.long, requires_grad=False)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('weight', {'weight': make_weight(10)}),
    ]

    def multilabelsoftmargin_loss_reference_fn(m, p, i, t, reduction='mean', weight=None):
        result = t * i.sigmoid().log() + (1 - t) * (-i).sigmoid().log()
        if weight is not None:
            result *= weight
        result = (-result).sum(i.dim() - 1) / i.size(-1)

        if reduction == 'none':
            return result
        elif reduction == 'mean':
            return result.mean()
        else:
            return result.sum()

    module_inputs = []
    for desc, constructor_kwargs in cases:
        module_inputs.append(
            ModuleInput(constructor_input=FunctionInput(**constructor_kwargs),
                        forward_input=FunctionInput(make_input((5, 10)),
                                                    make_target((5, 10), low=0, high=2)),
                        desc=desc,
                        reference_fn=partial(multilabelsoftmargin_loss_reference_fn, **constructor_kwargs))
        )

    return module_inputs

