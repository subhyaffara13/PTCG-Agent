
def validate_jupytext_configuration_file(config_file, config_dict):
    """Turn a dict-like config into a JupytextConfiguration object"""
    if config_dict is None:
        return None
    try:
        config = JupytextConfiguration(**config_dict)
    except TraitError as err:
        raise JupytextConfigurationError(f"The Jupytext configuration file {config_file} is incorrect: {err}")
    invalid_options = set(config_dict).difference(dir(JupytextConfiguration()))
    if any(invalid_options):
        raise JupytextConfigurationError(
            "The Jupytext configuration file {} is incorrect: options {} are not supported".format(
                config_file, ",".join(invalid_options)
            )
        )
    return config

