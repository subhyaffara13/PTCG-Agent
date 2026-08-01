
def get_optimizer_group(self, param: str | torch.nn.parameter.Parameter | None = None):
    """
    Returns optimizer group for a parameter if given, else returns all optimizer groups for params.

    Args:
        param (`str` or `torch.nn.parameter.Parameter`, *optional*):
            The parameter for which optimizer group needs to be returned.
    """
    if self.optimizer is None:
        raise ValueError("Trainer optimizer is None, please make sure you have setup the optimizer before.")
    if param is not None:
        for group in self.optimizer.param_groups:
            if param in group["params"]:
                return group
    return [group["params"] for group in self.optimizer.param_groups]

