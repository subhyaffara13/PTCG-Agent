
def _load_yaml_config(config_path: str) -> dict[str, Any]:
  """Loads a YAML configuration file."""
  logging.info('Loading configuration from: %s', config_path)
  try:
    with epath.Path(config_path).open('r') as f:
      return yaml.safe_load(f)
  except yaml.YAMLError as e:
    logging.error('Error parsing YAML file: %s', e)
    raise
  except FileNotFoundError:
    logging.error('Configuration file not found: %s', config_path)
    raise

