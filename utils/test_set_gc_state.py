
def test_set_gc_state(gc_lock):
    with gc_lock:
        gc_status = gc.isenabled()
        try:
            for state in (True, False):
                gc.enable()
                set_gc_state(state)
                assert_equal(gc.isenabled(), state)
                gc.disable()
                set_gc_state(state)
                assert_equal(gc.isenabled(), state)
        finally:
            if gc_status:
                gc.enable()

