from typing import Any

def _get_schedule_free_optimizer(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get ScheduleFree optimizer."""
    if not is_schedulefree_available():
        raise ImportError(
            "You need to install `schedulefree` in order to use schedulefree optimizers. "
            "Install it with `pip install schedulefree.`"
        )
    from schedulefree import AdamWScheduleFree, SGDScheduleFree

    additional_optim_kwargs = {}
    require_warmup = True

    if ctx.args.optim == OptimizerNames.SCHEDULE_FREE_RADAM:
        if not is_schedulefree_available("1.4.0"):
            raise ImportError(
                "You need to install `schedulefree>=1.4.0` in order to use RAdamScheduleFree optimizer. "
                "Install it with `pip install schedulefree.`"
            )
        from schedulefree import RAdamScheduleFree

        optimizer_cls = RAdamScheduleFree
        additional_optim_kwargs = ctx.adam_kwargs
        require_warmup = False
    elif ctx.args.optim == OptimizerNames.SCHEDULE_FREE_ADAMW:
        optimizer_cls = AdamWScheduleFree
        additional_optim_kwargs = ctx.adam_kwargs
    elif ctx.args.optim == OptimizerNames.SCHEDULE_FREE_SGD:
        optimizer_cls = SGDScheduleFree
    else:
        raise ValueError("Invalid schedulefree optimizer")

    additional_optim_kwargs["weight_decay"] = ctx.args.weight_decay
    if require_warmup:
        additional_optim_kwargs["warmup_steps"] = ctx.args.warmup_steps
    additional_optim_kwargs.update(
        {
            "weight_lr_power": float(ctx.optim_args.get("weight_lr_power", 2.0)),
            "r": float(ctx.optim_args.get("r", 0.0)),
        }
    )
    ctx.optimizer_kwargs.update(additional_optim_kwargs)
    return optimizer_cls, ctx.optimizer_kwargs

