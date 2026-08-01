
def nn_module_supports_equalization(module) -> bool:
    """Checks if the torch.nn node supports equalization."""
    return type(module) in [nn.Linear, nn.Conv1d, nn.Conv2d, nn.Conv3d]

