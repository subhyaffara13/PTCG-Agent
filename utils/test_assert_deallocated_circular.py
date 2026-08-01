
def test_assert_deallocated_circular():
    class C:
        def __init__(self):
            self._circular = self
    with pytest.raises(ReferenceError):
        # Circular reference, no automatic garbage collection
        with assert_deallocated(C) as c:
            del c

