from pathlib import Path


def _get_access_token_from_file(path):
    if not path:
        return None

    token_path = Path(path)
    if not token_path.exists():
        return None

    token_value = token_path.read_text().strip()
    if not token_value:
        return None

    get_logger().debug(f'Using access token from file: "{path}"')
    return token_value

