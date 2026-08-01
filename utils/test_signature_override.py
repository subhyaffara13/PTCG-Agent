
def test_signature_override():
    caller = _test_ccallback.test_call_simple
    func = _test_ccallback.test_get_plus1_capsule()

    llcallable = LowLevelCallable(func, signature="bad signature")
    assert_equal(llcallable.signature, "bad signature")
    assert_raises(ValueError, caller, llcallable, 3)

    llcallable = LowLevelCallable(func, signature="double (double, int *, void *)")
    assert_equal(llcallable.signature, "double (double, int *, void *)")
    assert_equal(caller(llcallable, 3), 4)

