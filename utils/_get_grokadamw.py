from typing import Any

def _get_grokadamw(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get GrokAdamW optimizer."""
    if not is_grokadamw_available():
        raise ValueError("Please install grokadamw with `pip install grokadamw`")

    from grokadamw import GrokAdamW

    ctx.optimizer_kwargs.update(
        {
            "alpha_init": float(ctx.optim_args.get("alpha_init", 0.98)),
            "lamb": float(ctx.optim_args.get("lamb", 2.0)),
            "gamma": float(ctx.optim_args.get("gamma", 0.1)),
            "grokking_signal_decay_rate": float(ctx.optim_args.get("grokking_signal_decay_rate", 0.1)),
            "gradient_clipping": float(ctx.optim_args.get("gradient_clipping", 1.0)),
        }
    )
    return GrokAdamW, ctx.optimizer_kwargs

