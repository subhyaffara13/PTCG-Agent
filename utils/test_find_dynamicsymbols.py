
def test_find_dynamicsymbols():
    a, b = symbols('a, b')
    x, y, z = dynamicsymbols('x, y, z')
    expr = Matrix([[a*x + b, x*y.diff() + y],
                   [x.diff().diff(), z + sin(z.diff())]])
    # Test finding all dynamicsymbols
    sol = {x, y.diff(), y, x.diff().diff(), z, z.diff()}
    assert find_dynamicsymbols(expr) == sol
    # Test finding all but those in sym_list
    exclude_list = [x, y, z]
    sol = {y.diff(), x.diff().diff(), z.diff()}
    assert find_dynamicsymbols(expr, exclude=exclude_list) == sol
    # Test finding all dynamicsymbols in a vector with a given reference frame
    d, e, f = dynamicsymbols('d, e, f')
    A = ReferenceFrame('A')
    v = d * A.x + e * A.y + f * A.z
    sol = {d, e, f}
    assert find_dynamicsymbols(v, reference_frame=A) == sol
    # Test if a ValueError is raised on supplying only a vector as input
    raises(ValueError, lambda: find_dynamicsymbols(v))

