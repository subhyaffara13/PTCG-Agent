
def test_FiniteSet_complex():
    from sympy.sets.sets import FiniteSet
    a, b, c, x, y, z = symbols('a,b,c,x,y,z')
    expr = FiniteSet(Basic(S(1), x), y, Basic(x, z))
    pattern = FiniteSet(a, Basic(x, b))
    variables = a, b
    expected = ({b: 1, a: FiniteSet(y, Basic(x, z))},
                      {b: z, a: FiniteSet(y, Basic(S(1), x))})
    assert iterdicteq(unify(expr, pattern, variables=variables), expected)

