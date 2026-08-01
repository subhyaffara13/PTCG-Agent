
def pep440(version: str) -> bool:
    """See :ref:`PyPA's version specification <pypa:version-specifiers>`
    (initially introduced in :pep:`440`).
    """
    return VERSION_REGEX.match(version) is not None

