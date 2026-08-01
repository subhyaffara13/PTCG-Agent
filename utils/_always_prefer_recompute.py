
def _always_prefer_recompute(ctx, op, *args, **kwargs):
    from torch.utils.checkpoint import CheckpointPolicy

    return CheckpointPolicy.PREFER_RECOMPUTE

