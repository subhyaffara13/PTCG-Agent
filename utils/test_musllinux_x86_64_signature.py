
def test_musllinux_x86_64_signature():
    # this test may fail if you're emulating musllinux_x86_64 on a different
    # architecture, but should pass natively.
    known_sigs = [b'\xcd\xcc\xcc\xcc\xcc\xcc\xcc\xcc\xfb\xbf']
    sig = (np.longdouble(-1.0) / np.longdouble(10.0))
    sig = sig.view(sig.dtype.newbyteorder('<')).tobytes()[:10]
    assert sig in known_sigs

