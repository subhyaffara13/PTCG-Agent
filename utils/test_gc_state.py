
def test_gc_state(gc_lock):
    # Test gc_state context manager
    with gc_lock:
        gc_status = gc.isenabled()
        try:
            for pre_state in (True, False):
                set_gc_state(pre_state)
                for with_state in (True, False):
                    # Check the gc state is with_state in with block
                    with gc_state(with_state):
                        assert_equal(gc.isenabled(), with_state)
                    # And returns to previous state outside block
                    assert_equal(gc.isenabled(), pre_state)
                    # Even if the gc state is set explicitly within the block
                    with gc_state(with_state):
                        assert_equal(gc.isenabled(), with_state)
                        set_gc_state(not with_state)
                    assert_equal(gc.isenabled(), pre_state)
        finally:
            if gc_status:
                gc.enable()

