
def test_rm_id():
    rmzeros = rm_id(lambda x: x == 0)
    assert rmzeros(Basic(S(0), S(1))) == Basic(S(1))
    assert rmzeros(Basic(S(0), S(0))) == Basic(S(0))
    assert rmzeros(Basic(S(2), S(1))) == Basic(S(2), S(1))

