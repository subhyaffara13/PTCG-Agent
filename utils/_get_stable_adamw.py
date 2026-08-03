from typing import Any

def _get_stable_adamw(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get StableAdamW optimizer from torch-optimi."""
    if not is_torch_optimi_available():
        raise ImportError(
            "You need to install `torch-optimi` in order to use stable_adamw optimizers. "
            "Install it with `pip install torch-optimi`."
        )
    from optimi import StableAdamW

    max_lr = ctx.optim_args.pop("max_lr", None)
    if max_lr is not None:
        max_lr = float(max_lr)

    kahan_sum = ctx.optim_args.pop("kahan_sum", None)
    if kahan_sum is not None:
        kahan_sum = bool(kahan_sum)

    ctx.adam_kwargs["weight_decay"] = ctx.args.weight_decay
    stable_adamw_kwargs = {
        "decouple_lr": bool(ctx.optim_args.pop("decouple_lr", False)),
        "max_lr": max_lr,
        "kahan_sum": kahan_sum,
    }

    ctx.optimizer_kwargs.update(ctx.adam_kwargs)
    ctx.optimizer_kwargs.update(stable_adamw_kwargs)
    return StableAdamW, ctx.optimizer_kwargs

