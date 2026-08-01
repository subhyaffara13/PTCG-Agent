
def is_pandoc_available(min_version="2.7.2", max_version=None):
    """Is Pandoc>=2.7.2 available?"""
    try:
        raise_if_pandoc_is_not_available(min_version=min_version, max_version=max_version)
        return True
    except PandocError:
        return False

