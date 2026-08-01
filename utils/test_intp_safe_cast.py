
def test_intp_safe_cast(ufunc):
    int_chars = {'i', 'l', 'q'}
    int_input = [set(sig.split('->')[0]) & int_chars for sig in ufunc.types]
    int_char = ''.join(s.pop() if s else '' for s in int_input)
    assert len(int_char) == 1, "More integer types in the signatures than expected"
    assert np.can_cast(np.intp, np.dtype(int_char))

