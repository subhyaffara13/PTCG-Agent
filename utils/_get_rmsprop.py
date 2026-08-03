from typing import Any

def _get_rmsprop(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get RMSprop optimizer."""
    kwargs = ctx.optimizer_kwargs.copy()
    if ctx.optim_args:
        for key in ("momentum", "alpha", "eps", "weight_decay"):
            if key in ctx.optim_args:
                kwargs[key] = float(ctx.optim_args[key])
        if "centered" in ctx.optim_args:
            kwargs["centered"] = ctx.optim_args["centered"].lower() in ("true", "1", "yes")
    return torch.optim.RMSprop, kwargs

