
def loggers_set_save_activations(
    model: torch.nn.Module,
    save_activations: bool,
) -> None:
    """
    Sets the `save_activations` setting on a `model`'s loggers
    """
    for _name, child in model.named_modules():
        if isinstance(child, OutputLogger):
            child.save_activations = save_activations

