from typing import Any

def config_from_dict(config: dict[str, Any]) -> Config:
    config = {**config}
    return Config(config, **_pop_config_kwargs(config))

