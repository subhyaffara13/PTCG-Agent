
def test_subs_dict():
    a, b, c, d, e = symbols('a b c d e')

    assert (2*x + y + z).subs({"x": 1, "y": 2}) == 4 + z

    l = [(sin(x), 2), (x, 1)]
    assert (sin(x)).subs(l) == \
           (sin(x)).subs(dict(l)) == 2
    assert sin(x).subs(reversed(l)) == sin(1)

    expr = sin(2*x) + sqrt(sin(2*x))*cos(2*x)*sin(exp(x)*x)
    reps = {sin(2*x): c,
               sqrt(sin(2*x)): a,
               cos(2*x): b,
               exp(x): e,
               x: d,}
    assert expr.subs(reps) == c + a*b*sin(d*e)

    l = [(x, 3), (y, x**2)]
    assert (x + y).subs(l) == 3 + x**2
    assert (x + y).subs(reversed(l)) == 12

    # If changes are made to convert lists into dictionaries and do
    # a dictionary-lookup replacement, these tests will help to catch
    # some logical errors that might occur
    l = [(y, z + 2), (1 + z, 5), (z, 2)]
    assert (y - 1 + 3*x).subs(l) == 5 + 3*x
    l = [(y, z + 2), (z, 3)]
    assert (y - 2).subs(l) == 3

