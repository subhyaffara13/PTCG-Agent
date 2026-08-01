
def _get_adagrad(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get Adagrad optimizer."""
    kwargs = ctx.optimizer_kwargs.copy()
    if ctx.optim_args:
        for key in ("lr_decay", "weight_decay", "eps"):
            if key in ctx.optim_args:
                kwargs[key] = float(ctx.optim_args[key])
    return torch.optim.Adagrad, kwargs

