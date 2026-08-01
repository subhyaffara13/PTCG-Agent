
def _get_fusion_pattern_to_fuse_handler_cls(
    backend_config: BackendConfig,
) -> dict[Pattern, Callable]:
    fusion_pattern_to_fuse_handlers: dict[Pattern, Callable] = {}
    for pattern, config in backend_config._pattern_complex_format_to_config.items():
        if config.fuser_method is not None:
            # TODO: is this logic right?
            fusion_pattern_to_fuse_handlers[pattern] = DefaultFuseHandler
    return fusion_pattern_to_fuse_handlers

