import re

def filter_files(prefix, suffix, files, remove_prefix=None):
    """
    Filter files by prefix and suffix.
    """
    filtered, rest = [], []
    match = re.compile(prefix + r'.*' + suffix + r'\Z').match
    if remove_prefix:
        ind = len(prefix)
    else:
        ind = 0
    for file in [x.strip() for x in files]:
        if match(file):
            filtered.append(file[ind:])
        else:
            rest.append(file)
    return filtered, rest

