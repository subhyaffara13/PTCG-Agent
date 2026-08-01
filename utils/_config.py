
def _config(
    path: Path | None = None, config: Config = DEFAULT_CONFIG, **config_kwargs: Any
) -> Config:
    if path and (
        config is DEFAULT_CONFIG
        and "settings_path" not in config_kwargs
        and "settings_file" not in config_kwargs
    ):
        config_kwargs["settings_path"] = path

    if config_kwargs:
        if config is not DEFAULT_CONFIG:
            raise ValueError(
                "You can either specify custom configuration options using kwargs or "
                "passing in a Config object. Not Both!"
            )

        config = Config(**config_kwargs)

    return config

