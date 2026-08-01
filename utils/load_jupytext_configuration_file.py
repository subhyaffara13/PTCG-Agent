
def load_jupytext_configuration_file(config_file, stream=None):
    """Read and validate a Jupytext configuration file, and return a JupytextConfiguration object"""
    config_dict = parse_jupytext_configuration_file(config_file, stream)
    config = validate_jupytext_configuration_file(config_file, config_dict)
    config.formats = normalize_formats(config.formats or config.default_jupytext_formats)

    if isinstance(config.notebook_extensions, str):
        config.notebook_extensions = config.notebook_extensions.split(",")
    return config

