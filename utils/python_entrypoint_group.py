
def python_entrypoint_group(value: str) -> bool:
    """See ``Data model > group`` in the :ref:`PyPA's entry-points specification
    <pypa:entry-points>`.
    """
    return ENTRYPOINT_GROUP_REGEX.match(value) is not None

