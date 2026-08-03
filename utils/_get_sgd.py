from typing import Any

def _get_sgd(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get SGD optimizer."""
    kwargs = ctx.optimizer_kwargs.copy()
    if ctx.optim_args:
        for key in ("momentum", "dampening", "weight_decay"):
            if key in ctx.optim_args:
                kwargs[key] = float(ctx.optim_args[key])
        if "nesterov" in ctx.optim_args:
            kwargs["nesterov"] = ctx.optim_args["nesterov"].lower() in ("true", "1", "yes")
    return torch.optim.SGD, kwargs

