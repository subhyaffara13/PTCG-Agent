
def git_timestamp(path):
    if not os.path.isfile(path):
        return None

    # Files that are in the git index are considered most recent
    if file_in_git_index(path):
        return float("inf")

    # Return the commit timestamp
    try:
        git_ts_str = system("git", "log", "-1", "--pretty=%ct", "--no-show-signature", path).strip()
    except SystemExit as err:
        if err.code == 128:
            # git not initialized
            git_ts_str = ""
        else:
            raise

    if git_ts_str:
        return float(git_ts_str)

    # The file is not in the git index
    return get_timestamp(path)

