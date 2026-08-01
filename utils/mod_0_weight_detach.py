
def mod_0_weight_detach(mod: nn.Module) -> torch.Tensor:
    return mod[0].weight.detach()  # type: ignore[index]

