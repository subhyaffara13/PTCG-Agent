
def test_bad_callback():
    e = a
    raises(ValueError, lambda: g.llvm_callable([a], e, callback_type='bad_callback'))

