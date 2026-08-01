
def test_index_permutations_with_dummies():
    a, b, c, d = symbols('a b c d')
    p, q, r, s = symbols('p q r s', cls=Dummy)
    f, g = map(Function, 'fg')
    P = PermutationOperator

    # No dummy substitution necessary
    expr = f(a, b, p, q) - f(b, a, p, q)
    assert simplify_index_permutations(
        expr, [P(a, b)]) == P(a, b)*f(a, b, p, q)

    # Cases where dummy substitution is needed
    expected = P(a, b)*substitute_dummies(f(a, b, p, q))

    expr = f(a, b, p, q) - f(b, a, q, p)
    result = simplify_index_permutations(expr, [P(a, b)])
    assert expected == substitute_dummies(result)

    expr = f(a, b, q, p) - f(b, a, p, q)
    result = simplify_index_permutations(expr, [P(a, b)])
    assert expected == substitute_dummies(result)

    # A case where nothing can be done
    expr = f(a, b, q, p) - g(b, a, p, q)
    result = simplify_index_permutations(expr, [P(a, b)])
    assert expr == result

