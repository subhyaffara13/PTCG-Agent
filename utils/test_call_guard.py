
def test_call_guard():
    assert m.unguarded_call() == "unguarded"
    assert m.guarded_call() == "guarded"

    assert m.multiple_guards_correct_order() == "guarded & guarded"
    assert m.multiple_guards_wrong_order() == "unguarded & guarded"

    if hasattr(m, "with_gil"):
        assert m.with_gil() == "GIL held"
        assert m.without_gil() == "GIL released"

