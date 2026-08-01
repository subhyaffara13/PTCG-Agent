
def load_cli_token() -> Optional[dict]:
    """Load CLI token data from file"""
    token_file = get_cli_token_file_path()
    if not os.path.exists(token_file):
        return None

    try:
        with open(token_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

