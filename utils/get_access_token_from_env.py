
def get_access_token_from_env():
    if is_in_kaggle_notebook():
        token = _get_access_token_from_file(os.environ.get(KAGGLE_API_V1_TOKEN_PATH))
        if token:
            return (token, KAGGLE_API_V1_TOKEN_PATH)

    access_token = os.environ.get("KAGGLE_API_TOKEN")
    if access_token:
        if Path(access_token).exists():
            return (_get_access_token_from_file(access_token), "KAGGLE_API_TOKEN")
        get_logger().debug(
            "Using access token from KAGGLE_API_TOKEN environment variable"
        )
        return (access_token, "KAGGLE_API_TOKEN")

    access_token = _get_access_token_from_file(os.path.expanduser("~/.kaggle/access_token"))
    if access_token:
        return (access_token, "access_token")

    # Check ".txt" as well in case Windows users create the file with this extension.
    access_token = _get_access_token_from_file(os.path.expanduser("~/.kaggle/access_token.txt"))
    if access_token:
        return (access_token, "access_token")

    return (None, None)

