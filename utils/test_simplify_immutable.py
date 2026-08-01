
def test_simplify_immutable():
    assert simplify(ImmutableMatrix([[sin(x)**2 + cos(x)**2]])) == \
                    ImmutableMatrix([[1]])

