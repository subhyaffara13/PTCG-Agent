
def test_AppliedUndef():
    """ Test printing AppliedUndef instance, which works similarly to Symbol. """
    ftt = aesara_code_(f_t)
    assert isinstance(ftt, TensorVariable)
    assert ftt.broadcastable == ()
    assert ftt.name == 'f_t'


def test_AppliedUndef():
    """ Test printing AppliedUndef instance, which works similarly to Symbol. """
    ftt = theano_code_(f_t)
    assert isinstance(ftt, tt.TensorVariable)
    assert ftt.broadcastable == ()
    assert ftt.name == 'f_t'

