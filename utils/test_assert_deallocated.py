
def test_assert_deallocated(gc_lock):
    # Ordinary use
    class C:
        def __init__(self, arg0, arg1, name='myname'):
            self.name = name
    with gc_lock:
        for gc_current in (True, False):
            with gc_state(gc_current):
                # We are deleting from with-block context, so that's OK
                with assert_deallocated(C, 0, 2, 'another name') as c:
                    assert_equal(c.name, 'another name')
                    del c
                # Or not using the thing in with-block context, also OK
                with assert_deallocated(C, 0, 2, name='third name'):
                    pass
                assert_equal(gc.isenabled(), gc_current)

