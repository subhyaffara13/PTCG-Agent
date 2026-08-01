
def should_exclude_file(filename) -> bool:
    for exclude_suffix in exclude_files:
        if filename.endswith(exclude_suffix):
            return True
    return False

