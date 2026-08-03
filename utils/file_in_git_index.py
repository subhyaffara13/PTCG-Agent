import os

def file_in_git_index(path):
    if not os.path.isfile(path):
        return False
    return system("git", "status", "--porcelain", path).strip().startswith(("M", "A"))

