
def is_within_directory(directory: str, target: str) -> bool:
    """
    Return true if the absolute path of target is within the directory
    (including when target is equal to the directory).
    """
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    return abs_target == abs_directory or abs_target.startswith(abs_directory + os.sep)

