
def separator(path):
    """Return the local path separator (always / in the contents manager)"""
    if os.path.sep == "\\" and "\\" in path:
        return "\\"
    return "/"

