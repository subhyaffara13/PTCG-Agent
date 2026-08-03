from typing import Any

def _get_adamw_torch_xla(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get Torch XLA syncfree AdamW optimizer."""
    try:
        from torch_xla.amp.syncfree import AdamW

        ctx.optimizer_kwargs.update(ctx.adam_kwargs)
        return AdamW, ctx.optimizer_kwargs
    except ImportError:
        raise ValueError("Trainer failed to import syncfree AdamW from torch_xla.")

