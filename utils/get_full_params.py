
def get_full_params(model: nn.Module, recurse: bool = True):
    """
    Returns the full unsharded parameters of ``model``. Any FSDP-managed
    parameters offloaded to CPU are moved to GPU in the returned list.

    Args:
        recurse (bool): If ``False``, only unshards the parameters immediate to
            ``model``; if ``True``, recurses through the module hierarchy
            rooted at ``model``.
    """
    with FSDP.summon_full_params(model, recurse=recurse):
        return deepcopy(list(model.parameters()))

