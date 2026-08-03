import os
from typing import Any

def _find_config(path: str) -> tuple[str, dict[str, Any]]:
    current_directory = path
    tries = 0
    while current_directory and tries < MAX_CONFIG_SEARCH_DEPTH:
        for config_file_name in CONFIG_SOURCES:
            potential_config_file = os.path.join(current_directory, config_file_name)
            if os.path.isfile(potential_config_file):
                config_data: dict[str, Any]
                try:
                    config_data = _get_config_data(
                        potential_config_file, CONFIG_SECTIONS[config_file_name]
                    )
                except Exception:
                    warn(
                        f"Failed to pull configuration information from {potential_config_file}",
                        stacklevel=2,
                    )
                    config_data = {}
                if config_data:
                    return (current_directory, config_data)

        for stop_dir in STOP_CONFIG_SEARCH_ON_DIRS:
            if os.path.isdir(os.path.join(current_directory, stop_dir)):
                return (current_directory, {})

        new_directory = os.path.split(current_directory)[0]
        if new_directory == current_directory:
            break

        current_directory = new_directory
        tries += 1

    return (path, {})

