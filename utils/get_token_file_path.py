from pathlib import Path


def get_token_file_path() -> str:
    """Get the path to store the authentication token"""
    home_dir = Path.home()
    config_dir = home_dir / ".litellm"
    config_dir.mkdir(exist_ok=True)
    return str(config_dir / "token.json")

