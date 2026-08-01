
def is_untracked(filepath):
    """Check whether a file was created or modified and needs to be added to the git index"""
    if not filepath:
        return False

    output = system("git", "ls-files", filepath).strip()
    if output == "":
        return True

    output = system("git", "diff", filepath).strip()
    if output != "":
        return True

    return False

