
def safe_getattr(object: Any, name: str, default: Any) -> Any:
    """Like getattr but return default upon any Exception or any OutcomeException.

    Attribute access can potentially fail for 'evil' Python objects.
    See issue #214.
    It catches OutcomeException because of #2490 (issue #580), new outcomes
    are derived from BaseException instead of Exception (for more details
    check #2707).
    """
    from _pytest.outcomes import TEST_OUTCOME

    try:
        return getattr(object, name, default)
    except TEST_OUTCOME:
        return default

