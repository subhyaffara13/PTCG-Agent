
def mod_weight_detach(mod: nn.Module) -> torch.Tensor:
    return mod.weight.detach()  # type: ignore[operator]

