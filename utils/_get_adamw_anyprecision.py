
def _get_adamw_anyprecision(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get AnyPrecision AdamW optimizer."""
    try:
        from torchdistx.optimizers import AnyPrecisionAdamW

        ctx.optimizer_kwargs.update(ctx.adam_kwargs)
        ctx.optimizer_kwargs.update(
            {
                "use_kahan_summation": strtobool(ctx.optim_args.get("use_kahan_summation", "False")),
                "momentum_dtype": getattr(torch, ctx.optim_args.get("momentum_dtype", "float32")),
                "variance_dtype": getattr(torch, ctx.optim_args.get("variance_dtype", "float32")),
                "compensation_buffer_dtype": getattr(
                    torch, ctx.optim_args.get("compensation_buffer_dtype", "bfloat16")
                ),
            }
        )
        return AnyPrecisionAdamW, ctx.optimizer_kwargs
    except ImportError:
        raise ValueError("Please install https://github.com/pytorch/torchdistx")

