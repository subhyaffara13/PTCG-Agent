
def python_entrypoint_name(value: str) -> bool:
    """See ``Data model > name`` in the :ref:`PyPA's entry-points specification
    <pypa:entry-points>`.
    """
    if not ENTRYPOINT_REGEX.match(value):
        return False
    if not RECOMMEDED_ENTRYPOINT_REGEX.match(value):
        msg = f"Entry point `{value}` does not follow recommended pattern: "
        msg += RECOMMEDED_ENTRYPOINT_PATTERN
        _logger.warning(msg)
    return True

