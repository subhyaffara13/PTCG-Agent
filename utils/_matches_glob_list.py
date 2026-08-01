
def _matches_glob_list(filename, glob_list):
    for glob in glob_list:
        if fnmatch.fnmatch(filename, glob):
            return True
    return False

