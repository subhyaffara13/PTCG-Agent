
def find_global_jupytext_configuration_file():
    """Return the global Jupytext configuration file, if any"""

    for config_dir in global_jupytext_configuration_directories():
        config_file = find_jupytext_configuration_file(config_dir, False)
        if config_file:
            return config_file

    return None

