
def _cast_buffers(mixed_precision_config, root_module):
    """Casts buffers to the given ``buffer_dtype``."""
    for buf in root_module.buffers():
        if hasattr(buf, "_ddp_ignored") and buf._ddp_ignored:
            continue

        buf.data = buf.to(dtype=mixed_precision_config.buffer_dtype)

