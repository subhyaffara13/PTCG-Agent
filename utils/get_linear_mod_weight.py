
def get_linear_mod_weight(mod: nn.Module) -> torch.Tensor:
    if isinstance(mod, nn.Linear):
        return mod.weight.detach()
    elif isinstance(mod, nni.LinearReLU):
        return mod[0].weight.detach()  # type: ignore[operator]
    else:
        return mod._weight_bias()[0]  # type: ignore[operator]

