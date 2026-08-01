
def set_fine_tuning_config(config):
    if config is None:
        return

    global fine_tuning_config
    if not isinstance(config, list):
        raise ValueError("invalid fine_tuning config, expected a list is not a list")

    for element in config:
        if isinstance(element, dict):
            for key, value in element.items():
                if isinstance(value, str) and value.startswith("os.environ/"):
                    element[key] = litellm.get_secret(value)

    fine_tuning_config = config

