from typing import Any

def _get_apollo_optimizer(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get Apollo optimizer."""
    if not is_apollo_torch_available():
        raise ImportError(
            "You need to install `apollo_torch` in order to use APOLLO optimizers. "
            "Install it with `pip install git+https://github.com/zhuhanqing/APOLLO`"
        )
    from apollo_torch import APOLLOAdamW

    optimizer_mapping = {
        OptimizerNames.APOLLO_ADAMW: APOLLOAdamW,
        OptimizerNames.APOLLO_ADAMW_LAYERWISE: APOLLOAdamW,
    }

    apollo_optim_kwargs = {
        "rank": int(ctx.optim_args.pop("rank", 128)),
        "proj": ctx.optim_args.pop("proj", "random"),
        "scale_type": ctx.optim_args.pop("scale_type", "channel"),
        "update_proj_gap": int(ctx.optim_args.pop("update_proj_gap", 200)),
        "scale": float(ctx.optim_args.pop("scale", 1.0)),
        "proj_type": ctx.optim_args.pop("proj_type", "std"),
    }
    apollo_optim_kwargs.update(ctx.adam_kwargs)

    return _setup_low_rank_optimizer(
        ctx.args, ctx.model, ctx.args.optim, optimizer_mapping, apollo_optim_kwargs, ctx.optimizer_kwargs
    )

