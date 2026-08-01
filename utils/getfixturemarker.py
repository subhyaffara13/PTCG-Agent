
def getfixturemarker(obj: object) -> FixtureFunctionMarker | None:
    """Return fixturemarker or None if it doesn't exist"""
    if isinstance(obj, FixtureFunctionDefinition):
        return obj._fixture_function_marker
    return None

