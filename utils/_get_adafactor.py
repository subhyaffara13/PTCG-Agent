
def _get_adafactor(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get Adafactor optimizer."""
    ctx.optimizer_kwargs.update({"scale_parameter": False, "relative_step": False})
    return Adafactor, ctx.optimizer_kwargs

