
def config_to_dict(config: Config) -> dict[str, Any]:
    config_dict = {
        **config.kwargs,
        "num_warps": config.num_warps,
        "num_stages": config.num_stages,
    }
    if HAS_WARP_SPEC:
        config_dict.update(
            {
                "num_consumer_groups": getattr(config, "num_consumer_groups", 0),
                "num_buffers_warp_spec": getattr(config, "num_buffers_warp_spec", 0),
            }
        )
    return config_dict

