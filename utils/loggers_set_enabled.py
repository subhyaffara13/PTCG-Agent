
def loggers_set_enabled(model: torch.nn.Module, enabled: bool) -> None:
    """
    Sets the `enabled` setting on a `model`'s loggers
    """
    for _, child in model.named_modules():
        if isinstance(child, OutputLogger):
            child.enabled = enabled

