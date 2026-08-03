from typing import Any

def prepare_config(config: Type[BaseConfig], cls_name: str) -> None:
    if not isinstance(config.extra, Extra):
        try:
            config.extra = Extra(config.extra)
        except ValueError:
            raise ValueError(f'"{cls_name}": {config.extra} is not a valid value for "extra"')


def prepare_config(config: ConfigDict | dict[str, Any] | type[Any] | None) -> ConfigDict:
    """Create a `ConfigDict` instance from an existing dict, a class (e.g. old class-based config) or None.

    Args:
        config: The input config.

    Returns:
        A ConfigDict object created from config.
    """
    if config is None:
        return ConfigDict()

    if not isinstance(config, dict):
        warnings.warn(DEPRECATION_MESSAGE, PydanticDeprecatedSince20, stacklevel=4)
        config = {k: getattr(config, k) for k in dir(config) if not k.startswith('__')}

    config_dict = cast(ConfigDict, config)
    check_deprecated(config_dict)
    return config_dict

