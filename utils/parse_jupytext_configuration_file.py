import json

def parse_jupytext_configuration_file(jupytext_config_file, stream=None):
    """Read a Jupytext config file, and return a dict"""
    if not jupytext_config_file.endswith(".py") and stream is None:
        with open(jupytext_config_file, encoding="utf-8") as stream:
            return parse_jupytext_configuration_file(jupytext_config_file, stream.read())

    try:
        if jupytext_config_file.endswith((".toml", "jupytext")):
            doc = tomllib.loads(stream)
            if jupytext_config_file.endswith(PYPROJECT_FILE):
                return doc["tool"]["jupytext"]
            else:
                return doc

        if jupytext_config_file.endswith((".yml", ".yaml")):
            return yaml.safe_load(stream)

        if jupytext_config_file.endswith(".json"):
            return json.loads(stream)

        return PyFileConfigLoader(jupytext_config_file).load_config()
    except (ValueError, NameError) as err:
        raise JupytextConfigurationError(f"The Jupytext configuration file {jupytext_config_file} is incorrect: {err}")

