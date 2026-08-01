
def _get_adamw_torch_npu_fused(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get NPU Fused AdamW optimizer."""
    try:
        from torch_npu.optim import NpuFusedAdamW

        ctx.optimizer_kwargs.update(ctx.adam_kwargs)
        return NpuFusedAdamW, ctx.optimizer_kwargs
    except ImportError:
        raise ValueError("Trainer failed to import FusedAdamW from torch_npu.")

