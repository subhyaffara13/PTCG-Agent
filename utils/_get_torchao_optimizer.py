from typing import Any

def _get_torchao_optimizer(ctx: OptimizerContext) -> tuple[Any, dict[str, Any]]:
    """Get TorchAO 4-bit or 8-bit optimizer."""
    if not is_torchao_available() or version.parse(importlib.metadata.version("torchao")) < version.parse("0.4.0"):
        raise ImportError(
            "You need to have `torchao>=0.4.0` in order to use torch 4-bit optimizers. "
            "Install it with `pip install torchao` or follow the instructions here: "
            "https://github.com/pytorch/ao"
        )
    if version.parse(importlib.metadata.version("torch")) <= version.parse("2.4"):
        raise ImportError(
            "You need to have `torch>2.4` in order to use torch 4-bit optimizers. "
            "Install it with `pip install --upgrade torch` it is available on pipy. "
            "Otherwise, you need to install torch nightly."
        )

    if version.parse(importlib.metadata.version("torchao")) >= version.parse("0.11.0"):
        from torchao.optim import AdamW4bit, AdamW8bit
    else:
        from torchao.prototype.low_bit_optim import AdamW4bit, AdamW8bit

    if ctx.args.optim == OptimizerNames.ADAMW_TORCH_4BIT:
        optimizer_cls = AdamW4bit
    else:
        optimizer_cls = AdamW8bit

    ctx.optimizer_kwargs.update(
        {
            "block_size": ctx.optim_args.get("block_size", 256),
            "bf16_stochastic_round": strtobool(ctx.optim_args.get("bf16_stochastic_round", "False")),
        }
    )
    ctx.optimizer_kwargs.update(ctx.adam_kwargs)
    return optimizer_cls, ctx.optimizer_kwargs

