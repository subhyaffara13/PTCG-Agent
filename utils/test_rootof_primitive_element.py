
def test_rootof_primitive_element():
    r1 = rootof(x**3 + x + 1, 0)
    r2 = rootof(x**3 + x + 1, 1)
    K12 = QQ.algebraic_field(r1 + r2)
    assert construct_domain([r1, r2], extension=True) == (
            K12, [K12.from_sympy(r1), K12.from_sympy(r2)])

