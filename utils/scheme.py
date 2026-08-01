
def scheme(name):
    """
    Override the selected scheme for posix_prefix.
    """
    if not enabled() or not name.endswith('_prefix'):
        return name
    return 'osx_framework_library'

