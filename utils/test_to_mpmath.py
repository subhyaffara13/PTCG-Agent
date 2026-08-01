
def test_to_mpmath():
    assert sqrt(3)._to_mpmath(20)._mpf_ == (0, int(908093), -19, 20)
    assert S(3.2)._to_mpmath(20)._mpf_ == (0, int(838861), -18, 20)

