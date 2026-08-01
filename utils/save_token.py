
def save_token(token_data: Dict[str, Any]) -> None:
    """Save token data to file"""
    token_file = get_token_file_path()
    with open(token_file, "w") as f:
        json.dump(token_data, f, indent=2)
    # Set file permissions to be readable only by owner
    os.chmod(token_file, 0o600)

