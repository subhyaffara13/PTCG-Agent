from pathlib import Path


def get_cli_token_file_path() -> str:
    """Get the path to the CLI token file"""
    home_dir = Path.home()
    config_dir = home_dir / ".litellm"
    return str(config_dir / "token.json")

