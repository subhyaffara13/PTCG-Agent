
def identical_format_path(fmt1, fmt2):
    """Do the two (long representation) of formats target the same file?"""
    for key in ["extension", "prefix", "suffix"]:
        if fmt1.get(key) != fmt2.get(key):
            return False
    return True

