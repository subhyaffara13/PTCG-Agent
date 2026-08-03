import os
from typing import Any

def load_config(config_path: str) -> dict[str, Any]:
  """Loads and validates a benchmark YAML config into a raw dict.

  Args:
    config_path: Path to the YAML configuration file.

  Returns:
    The parsed, validated config dict.
  """
  config = _load_yaml_config(config_path)
  _validate_config(config)
  return config


def load_config(yaml_path: str) -> tiering_service_pb2.ServerConfig:
  """Loads and parses a ServerConfig from a YAML file.

  Args:
    yaml_path: Path to the YAML configuration file.

  Returns:
    A ServerConfig proto instance populated with the parsed data.
  """
  with open(yaml_path, "r") as f:
    config_dict = yaml.safe_load(f)
  return parse_config(config_dict)


def load_config(config_path):
    """Loads the configuration from a YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_config(config_path):
    """Loads the configuration from a YAML file."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_config(
    config: str | None,
    extra: list[str],
    *,
    isolated: bool = False,
) -> tuple[configparser.RawConfigParser, str]:
    """Load the configuration given the user options.

    - in ``isolated`` mode, return an empty configuration
    - if a config file is given in ``config`` use that, otherwise attempt to
      discover a configuration using ``tox.ini`` / ``setup.cfg`` / ``.flake8``
    - finally, load any ``extra`` configuration files
    """
    pwd = os.path.abspath(".")

    if isolated:
        return configparser.RawConfigParser(), pwd

    if config is None:
        config = _find_config_file(pwd)

    cfg = configparser.RawConfigParser()
    if config is not None:
        if not cfg.read(config, encoding="UTF-8"):
            raise exceptions.ExecutionError(
                f"The specified config file does not exist: {config}"
            )
        cfg_dir = os.path.dirname(config)
    else:
        cfg_dir = pwd

    # TODO: remove this and replace it with configuration modifying plugins
    # read the additional configs afterwards
    for filename in extra:
        if not cfg.read(filename, encoding="UTF-8"):
            raise exceptions.ExecutionError(
                f"The specified config file does not exist: {filename}"
            )

    return cfg, cfg_dir

