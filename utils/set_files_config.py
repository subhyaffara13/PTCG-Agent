
def set_files_config(config):
    global files_config
    if config is None:
        return

    if not isinstance(config, list):
        raise ValueError("invalid files config, expected a list is not a list")

    for element in config:
        if isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, str) and value.startswith("os.environ/"):
                    element[key] = get_secret_str(value)

    files_config = config

