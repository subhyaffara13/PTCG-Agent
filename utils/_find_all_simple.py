import os

def _find_all_simple(path):
    """
    Find all files under 'path'
    """
    results = (
        os.path.join(base, file)
        for base, dirs, files in os.walk(path, followlinks=True)
        for file in files
    )
    return filter(os.path.isfile, results)


def _find_all_simple(path):
    """
    Find all files under 'path'
    """
    all_unique = _UniqueDirs.filter(os.walk(path, followlinks=True))
    results = (
        os.path.join(base, file) for base, dirs, files in all_unique for file in files
    )
    return filter(os.path.isfile, results)

