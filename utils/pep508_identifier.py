
def pep508_identifier(name: str) -> bool:
    """See :ref:`PyPA's name specification <pypa:name-format>`
    (initially introduced in :pep:`508#names`).
    """
    return PEP508_IDENTIFIER_REGEX.match(name) is not None

