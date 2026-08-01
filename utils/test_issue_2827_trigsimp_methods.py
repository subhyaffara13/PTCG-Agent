
def test_issue_2827_trigsimp_methods():
    measure1 = lambda expr: len(str(expr))
    measure2 = lambda expr: -count_ops(expr)
                                       # Return the most complicated result
    expr = (x + 1)/(x + sin(x)**2 + cos(x)**2)
    ans = Matrix([1])
    M = Matrix([expr])
    assert trigsimp(M, method='fu', measure=measure1) == ans
    assert trigsimp(M, method='fu', measure=measure2) != ans
    # all methods should work with Basic expressions even if they
    # aren't Expr
    M = Matrix.eye(1)
    assert all(trigsimp(M, method=m) == M for m in
        'fu matching groebner old'.split())
    # watch for E in exptrigsimp, not only exp()
    eq = 1/sqrt(E) + E
    assert exptrigsimp(eq) == eq

