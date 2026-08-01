
def test_cot_AccumBounds():
    assert cot(AccumBounds(-oo, oo)) == AccumBounds(-oo, oo)
    assert cot(AccumBounds(-S.Pi/3, S.Pi/3)) == AccumBounds(-oo, oo)
    assert cot(AccumBounds(S.Pi/6, S.Pi/3)) == AccumBounds(cot(S.Pi/3), cot(S.Pi/6))

