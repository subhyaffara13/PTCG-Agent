
def simple_literal_type(t: ProperType | None) -> Instance | None:
    """Extract the underlying fallback Instance type for a simple Literal"""
    if isinstance(t, Instance) and t.last_known_value is not None:
        t = t.last_known_value
    if isinstance(t, LiteralType):
        return t.fallback
    return None

