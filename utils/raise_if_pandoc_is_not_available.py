
def raise_if_pandoc_is_not_available(min_version="2.7.2", max_version=None):
    """Raise with an informative error message if pandoc is not available"""
    version = pandoc_version()
    if version == "N/A":
        raise PandocError(f"The Pandoc Markdown format requires 'pandoc>={min_version}', but pandoc was not found")

    if parse(version) < parse(min_version):
        raise PandocError(
            f"The Pandoc Markdown format requires 'pandoc>={min_version}', but pandoc version {version} was found"
        )

    if max_version and parse(version) > parse(max_version):
        raise PandocError(
            f"The Pandoc Markdown format requires 'pandoc<={max_version}', but pandoc version {version} was found"
        )

    return version

