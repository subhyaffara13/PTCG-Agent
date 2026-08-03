from typing import Any

def _check_is_valid_config_dict(
    config_dict: Any, allowed_keys: set[str], dict_name: str
) -> None:
    r"""Checks if the given config_dict has the correct keys

    Args:
      `config_dict`: dictionary whose keys we want to check
    """

    for k in config_dict:
        if k not in allowed_keys:
            raise ValueError(
                "Expected "
                + dict_name
                + " to have the following keys: "
                + str(allowed_keys)
                + ". But found '"
                + k
                + "' instead."
            )

