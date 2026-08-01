
def get_patched_config_dict(
    config_patches: str | dict[str, Any] | None = None,
) -> dict[str, Any]:
    with config.patch(config_patches):
        return config.get_config_copy()

