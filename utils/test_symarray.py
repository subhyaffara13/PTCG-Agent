
def test_symarray():
    """Test creation of numpy arrays of SymPy symbols."""

    import numpy as np
    import numpy.testing as npt

    syms = symbols('_0,_1,_2')
    s1 = symarray("", 3)
    s2 = symarray("", 3)
    npt.assert_array_equal(s1, np.array(syms, dtype=object))
    assert s1[0] == s2[0]

    a = symarray('a', 3)
    b = symarray('b', 3)
    assert not(a[0] == b[0])

    asyms = symbols('a_0,a_1,a_2')
    npt.assert_array_equal(a, np.array(asyms, dtype=object))

    # Multidimensional checks
    a2d = symarray('a', (2, 3))
    assert a2d.shape == (2, 3)
    a00, a12 = symbols('a_0_0,a_1_2')
    assert a2d[0, 0] == a00
    assert a2d[1, 2] == a12

    a3d = symarray('a', (2, 3, 2))
    assert a3d.shape == (2, 3, 2)
    a000, a120, a121 = symbols('a_0_0_0,a_1_2_0,a_1_2_1')
    assert a3d[0, 0, 0] == a000
    assert a3d[1, 2, 0] == a120
    assert a3d[1, 2, 1] == a121

