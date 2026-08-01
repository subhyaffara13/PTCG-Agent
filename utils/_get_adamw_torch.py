
def _get_adamw_torch(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get PyTorch AdamW optimizer (regular or fused)."""
    from torch.optim import AdamW

    ctx.optimizer_kwargs.update(ctx.adam_kwargs)
    if ctx.args.optim == OptimizerNames.ADAMW_TORCH_FUSED:
        ctx.optimizer_kwargs.update({"fused": True})
    return AdamW, ctx.optimizer_kwargs

