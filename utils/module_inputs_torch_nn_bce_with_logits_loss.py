
def module_inputs_torch_nn_BCEWithLogitsLoss(module_info, device, dtype, requires_grad, training, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    make_target = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)
    make_weight = partial(make_tensor, device=device, dtype=dtype, requires_grad=False)

    cases: list[tuple[str, dict]] = [
        ('', {}),
        ('reduction_sum', {'reduction': 'sum'}),
        ('reduction_mean', {'reduction': 'mean'}),
        ('reduction_none', {'reduction': 'none'}),
        ('weights', {'weight': make_weight((10,))}),
        ('scalar_weights', {'weight': make_weight(())})
    ]

    def bce_withlogitsloss_reference_fn(m, p, i, t, reduction='mean', weight=None):
        # TODO: add pos_weight to the definition here and corresponding SampleInputs
        max_val = (-i).clamp(min=0)
        result = (1 - t).mul_(i).add_(max_val).add_((-max_val).exp_().add_((-i - max_val).exp_()).log_())

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
                        reference_fn=partial(bce_withlogitsloss_reference_fn, **constructor_kwargs))
        )

    return module_inputs

