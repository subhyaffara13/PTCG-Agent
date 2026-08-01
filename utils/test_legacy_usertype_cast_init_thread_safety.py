
def test_legacy_usertype_cast_init_thread_safety(rat_cls):
    def closure(b):
        b.wait()
        np.full((10, 10), 1, rat_cls)

    run_threaded(closure, 250, pass_barrier=True)

