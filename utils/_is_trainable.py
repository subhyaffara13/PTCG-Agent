
def _is_trainable(param: torch.Tensor) -> bool:
    r"""Return if a parameter is trainable, where trainability is equivalent to requiring a gradient."""
    return param.requires_grad

