
def get_conv_mod_weight(mod: nn.Module) -> torch.Tensor:
    if isinstance(mod, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
        return mod.weight.detach()
    elif isinstance(mod, (nni.ConvReLU1d, nni.ConvReLU2d, nni.ConvReLU3d)):
        return mod[0].weight.detach()  # type: ignore[operator]
    else:
        return mod._weight_bias()[0]  # type: ignore[operator]

