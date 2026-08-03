from typing import Any

def is_valid_string_storage(value: Any) -> None:
    legal_values = ["auto", "python", "pyarrow"]
    if value not in legal_values:
        msg = "Value must be one of python|pyarrow"
        raise ValueError(msg)

