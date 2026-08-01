
def test_MatAdd_postprocessor_xfail():
    # This is difficult to get working because of the way that Add processes
    # its args.
    z = zeros(2)
    assert Add(z, S.NaN) == Add(S.NaN, z)

