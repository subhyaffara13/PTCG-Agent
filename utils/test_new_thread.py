
def test_new_thread():
    import threading
    t = threading.Thread()
    t_ = dill.copy(t)
    assert t.is_alive() == t_.is_alive()
    for i in ['daemon','name','ident','native_id']:
        if hasattr(t, i):
            assert getattr(t, i) == getattr(t_, i)

