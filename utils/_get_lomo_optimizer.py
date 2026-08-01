
def _get_lomo_optimizer(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get LOMO optimizer."""
    if not is_lomo_available():
        raise ImportError(
            "You need to install `lomo_optim` in order to use LOMO optimizers. "
            "Install it with `pip install lomo-optim`"
        )

    if ctx.model is None:
        raise ValueError("You need to pass a `model` in order to correctly initialize a LOMO optimizer.")

    from lomo_optim import AdaLomo, Lomo

    optimizer_cls = AdaLomo if "ada" in ctx.args.optim else Lomo
    ctx.optimizer_kwargs.update({"model": ctx.model})
    return optimizer_cls, ctx.optimizer_kwargs

