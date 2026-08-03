import re

def test_no_placement_new(capture):
    """Prior to 2.2, `py::init<...>` relied on the type supporting placement
    new; this tests a class without placement new support."""
    with capture:
        a = m.NoPlacementNew(123)

    found = re.search(r"^operator new called, returning (\d+)\n$", str(capture))
    assert found
    assert a.i == 123
    with capture:
        del a
        pytest.gc_collect()
    assert capture == "operator delete called on " + found.group(1)

    with capture:
        b = m.NoPlacementNew()

    found = re.search(r"^operator new called, returning (\d+)\n$", str(capture))
    assert found
    assert b.i == 100
    with capture:
        del b
        pytest.gc_collect()
    assert capture == "operator delete called on " + found.group(1)

