
def group_dir(group_name: str) -> str:
    """Given a group name, return the relative directory path for it."""
    return os.sep.join(group_name.split(".")[:-1])

