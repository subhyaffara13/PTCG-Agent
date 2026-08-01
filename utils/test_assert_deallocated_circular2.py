
def test_assert_deallocated_circular2():
    class C:
        def __init__(self):
            self._circular = self
    with pytest.raises(ReferenceError):
        # Still circular reference, no automatic garbage collection
        with assert_deallocated(C):
            pass

