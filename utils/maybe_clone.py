
def maybe_clone(x: torch.Tensor | None) -> torch.Tensor | None:
    if x is not None:
        return clone_preserve_strides(x)
    return x

