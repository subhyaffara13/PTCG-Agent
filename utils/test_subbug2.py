
def test_subbug2():
    # Ensure this does not cause infinite recursion
    assert Float(7.7).epsilon_eq(abs(x).subs(x, -7.7))

