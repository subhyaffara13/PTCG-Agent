
def test_pretty():
    assert pretty(Q.positive(x)) == "Q.positive(x)"
    assert pretty(
        {Q.positive, Q.integer}) == "{Q.integer, Q.positive}"


def test_pretty():
    mp.pretty = True
    assert repr(mpf(2.5)) == '2.5'
    assert repr(mpc(2.5,3.5)) == '(2.5 + 3.5j)'
    mp.pretty = False
    iv.pretty = True
    assert repr(mpi(2.5,3.5)) == '[2.5, 3.5]'
    iv.pretty = False

