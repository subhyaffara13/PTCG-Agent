
def _maybe_wrap_fsdp(model: nn.Module, wrap_fsdp: bool, *args, **kwargs):
    return model if not wrap_fsdp else FSDP(model, *args, **kwargs)

