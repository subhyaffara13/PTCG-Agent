
def gc_tester():
    """Tests that an object is garbage collected.

    Assumes that any unreferenced objects are fully collected after calling
    `gc.collect()`.  That is true on CPython, but does not appear to reliably
    hold on PyPy.
    """

    weak_refs = []

    def add_ref(obj):
        # PyPy does not support `gc.is_tracked`.
        if hasattr(gc, "is_tracked"):
            assert gc.is_tracked(obj)
        weak_refs.append(weakref.ref(obj))

    yield add_ref

    gc.collect()
    for ref in weak_refs:
        assert ref() is None

