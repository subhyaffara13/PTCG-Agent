
def _validate_dynamo_config_keys(config_str: str) -> str | None:
    """Return an error message if any config key is invalid, else None."""
    router = GraphConfigRouter(config_str)
    from torch._dynamo import config

    for _, config_dict in router._rules:
        for key in config_dict:
            if not hasattr(config, key):
                return (
                    f"TORCH_COMPILE_OVERRIDE_DYNAMO_CONFIGS: "
                    f"'{key}' is not a valid torch._dynamo.config option"
                )
    return None

