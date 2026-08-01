
def check_files(files, file_check, exclusions=set(), pattern=None):
    """
    Checks all files with the file_check function provided, skipping files
    that contain any of the strings in the set provided by exclusions.
    """
    if not files:
        return
    for fname in files:
        if not exists(fname) or not isfile(fname):
            continue
        if any(ex in fname for ex in exclusions):
            continue
        if pattern is None or re.match(pattern, fname):
            file_check(fname)

