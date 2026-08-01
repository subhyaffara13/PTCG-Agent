
def _use_template_for_gpu(
    layout: Layout, allowed_layout_dtypes: list[torch.dtype]
) -> bool:
    if layout.dtype not in allowed_layout_dtypes:
        log.debug(
            "Not using template since dtype %s is not in allowed layout dtypes %s",
            layout.dtype,
            allowed_layout_dtypes,
        )
    return (
        is_gpu(layout.device.type)
        and layout.dtype in allowed_layout_dtypes
        and is_big_gpu(layout.device)
    )

