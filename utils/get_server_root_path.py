
def get_server_root_path() -> str:
    """
    Get the server root path from the environment variables.

    - If SERVER_ROOT_PATH is set, return it.
    - Otherwise, default to "/".
    """
    return os.getenv("SERVER_ROOT_PATH", "")

