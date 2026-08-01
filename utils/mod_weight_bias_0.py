
def mod_weight_bias_0(mod: nn.Module) -> torch.Tensor:
    return mod._weight_bias()[0]  # type: ignore[operator]

