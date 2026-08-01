
def get_abi3_suffix():
    """Return the file extension for an abi3-compliant Extension()"""
    for suffix in EXTENSION_SUFFIXES:
        if '.abi3' in suffix:  # Unix
            return suffix
        elif suffix == '.pyd':  # Windows
            return suffix
    return None

