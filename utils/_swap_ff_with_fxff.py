
def _swap_ff_with_fxff(model: torch.nn.Module) -> None:
    r"""Swap FloatFunctional with FXFloatFunctional"""
    modules_to_swap = []
    for name, module in model.named_children():
        if isinstance(module, torch.ao.nn.quantized.FloatFunctional):
            modules_to_swap.append(name)
        else:
            _swap_ff_with_fxff(module)

    for name in modules_to_swap:
        del model._modules[name]
        model._modules[name] = torch.ao.nn.quantized.FXFloatFunctional()

