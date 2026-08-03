import os
from typing import Dict

def _read_opik_config_file() -> Dict[str, str]:
    config_path = os.path.expanduser(CONFIG_FILE_PATH_DEFAULT)

    config = configparser.ConfigParser()
    config.read(config_path)

    config_values = {
        section: dict(config.items(section)) for section in config.sections()
    }

    if "opik" in config_values:
        return config_values["opik"]

    return {}

