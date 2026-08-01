
def get_configuration_file(configuration_files: list[str]) -> str:
    """
    Get the configuration file to use for this version of transformers.

    Args:
        configuration_files (`list[str]`): The list of available configuration files.

    Returns:
        `str`: The configuration file to use.
    """
    configuration_files_map = {}
    for file_name in configuration_files:
        if file_name.startswith("config.") and file_name.endswith(".json") and file_name != "config.json":
            v = file_name.removeprefix("config.").removesuffix(".json")
            configuration_files_map[v] = file_name
    available_versions = sorted(configuration_files_map.keys())

    # Defaults to FULL_CONFIGURATION_FILE and then try to look at some newer versions.
    configuration_file = CONFIG_NAME
    transformers_version = version.parse(__version__)
    for v in available_versions:
        if version.parse(v) <= transformers_version:
            configuration_file = configuration_files_map[v]
        else:
            # No point going further since the versions are sorted.
            break

    return configuration_file

