import os

def clear_token() -> None:
    """Clear stored token"""
    token_file = get_token_file_path()
    if os.path.exists(token_file):
        os.remove(token_file)

