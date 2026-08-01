
def test_dim_simplify_rec():
    # assert Mul(Add(L, L), T) == L*T
    assert (L + L) * T == L*T

