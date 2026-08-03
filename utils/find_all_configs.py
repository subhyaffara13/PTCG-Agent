import os
from typing import Any

def find_all_configs(path: str) -> Trie:
    """
    Looks for config files in the path provided and in all of its sub-directories.
    Parses and stores any config file encountered in a trie and returns the root of
    the trie
    """
    trie_root = Trie("default", {})

    for dirpath, _, _ in os.walk(path):
        for config_file_name in CONFIG_SOURCES:
            potential_config_file = os.path.join(dirpath, config_file_name)
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
                    trie_root.insert(potential_config_file, config_data)
                    break

    return trie_root

