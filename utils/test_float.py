
def test_float(doc):
    assert doc(m.get_float) == "get_float() -> float"


def test_float(value: t.Any) -> bool:
    """Return true if the object is a float.

    .. versionadded:: 2.11
    """
    return isinstance(value, float)

