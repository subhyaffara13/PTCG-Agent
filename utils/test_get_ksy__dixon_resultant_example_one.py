
def test_get_KSY_Dixon_resultant_example_one():
    """Tests the KSY Dixon resultant for example one"""
    x, y, z = symbols('x, y, z')

    p = x * y * z
    q = x**2 - z**2
    h = x + y + z
    dixon = DixonResultant([p, q, h], [x, y])
    dixon_poly = dixon.get_dixon_polynomial()
    dixon_matrix = dixon.get_dixon_matrix(dixon_poly)
    D = dixon.get_KSY_Dixon_resultant(dixon_matrix)

    assert D == -z**3

