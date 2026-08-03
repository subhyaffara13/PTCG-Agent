from typing import Any

def _get_galore_optimizer(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get GaLore optimizer."""
    if not is_galore_torch_available():
        raise ImportError(
            "You need to install `galore_torch` in order to use GaLore optimizers. "
            "Install it with `pip install git+https://github.com/jiaweizzhao/GaLore`"
        )
    from galore_torch import GaLoreAdafactor, GaLoreAdamW, GaLoreAdamW8bit

    optimizer_mapping = {
        OptimizerNames.GALORE_ADAMW: GaLoreAdamW,
        OptimizerNames.GALORE_ADAMW_8BIT: GaLoreAdamW8bit,
        OptimizerNames.GALORE_ADAFACTOR: GaLoreAdafactor,
        OptimizerNames.GALORE_ADAMW_LAYERWISE: GaLoreAdamW,
        OptimizerNames.GALORE_ADAMW_8BIT_LAYERWISE: GaLoreAdamW8bit,
        OptimizerNames.GALORE_ADAFACTOR_LAYERWISE: GaLoreAdafactor,
    }

    galore_optim_kwargs = {
        "rank": int(ctx.optim_args.pop("rank", 128)),
        "update_proj_gap": int(ctx.optim_args.pop("update_proj_gap", 200)),
        "scale": float(ctx.optim_args.pop("scale", 0.25)),
        "proj_type": ctx.optim_args.pop("proj_type", "std"),
    }

    optimizer_cls, optimizer_kwargs = _setup_low_rank_optimizer(
        ctx.args, ctx.model, ctx.args.optim, optimizer_mapping, galore_optim_kwargs, ctx.optimizer_kwargs
    )
    if ctx.args.optim == OptimizerNames.GALORE_ADAFACTOR:
        optimizer_kwargs.update({"scale_parameter": False, "relative_step": False})
    return optimizer_cls, optimizer_kwargs

