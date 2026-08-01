
def _torch_load_weights_only(path: str, **kwargs):
    try:
        return torch.load(path, weights_only=True, **kwargs)
    except TypeError:
        logger.warning(
            "Current PyTorch version does not support torch.load(..., weights_only=True); "
            "falling back to default torch.load behavior for %s.",
            path,
        )
        return torch.load(path, **kwargs)

