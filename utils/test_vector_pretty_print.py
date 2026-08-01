
def test_vector_pretty_print():

    # TODO : The unit vectors should print with subscripts but they just
    # print as `n_x` instead of making `x` a subscript with unicode.

    # TODO : The pretty print division does not print correctly here:
    # w = alpha * N.x + sin(omega) * N.y + alpha / beta * N.z

    expected = """\
 2                               \n\
a  n_x + b n_y + c*sin(alpha) n_z\
"""
    uexpected = """\
 2                           \n\
a  n_x + b n_y + c⋅sin(α) n_z\
"""

    assert ascii_vpretty(v) == expected
    assert unicode_vpretty(v) == uexpected

    expected = 'alpha n_x + sin(omega) n_y + alpha*beta n_z'
    uexpected = 'α n_x + sin(ω) n_y + α⋅β n_z'

    assert ascii_vpretty(w) == expected
    assert unicode_vpretty(w) == uexpected

    expected = """\
                     2    \n\
a       b + c       c     \n\
- n_x + ----- n_y + -- n_z\n\
b         a         b     \
"""
    uexpected = """\
                     2    \n\
a       b + c       c     \n\
─ n_x + ───── n_y + ── n_z\n\
b         a         b     \
"""

    assert ascii_vpretty(o) == expected
    assert unicode_vpretty(o) == uexpected

    # https://github.com/sympy/sympy/issues/26731
    assert ascii_vpretty(-A.x) == '-a_x'
    assert unicode_vpretty(-A.x) == '-a_x'

    # https://github.com/sympy/sympy/issues/26799
    assert ascii_vpretty(0*A.x) == '0'
    assert unicode_vpretty(0*A.x) == '0'

