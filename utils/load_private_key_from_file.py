from typing import Any

def load_private_key_from_file(file_path: str) -> Any:
    """Loads a private key from a file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            key_str = f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Private key file not found: {file_path}")
    except OSError as e:
        raise OSError(f"Failed to read private key file '{file_path}': {e}") from e

    if not key_str:
        raise ValueError(f"Private key file is empty: {file_path}")

    return load_private_key_from_str(key_str)

