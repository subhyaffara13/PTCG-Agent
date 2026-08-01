
def test_matrixSymbolBold():
    # Issue 15871
    def boldpretty(expr):
        return xpretty(expr, use_unicode=True, wrap_line=False, mat_symbol_style="bold")

    from sympy.matrices.expressions.trace import trace
    A = MatrixSymbol("A", 2, 2)
    assert boldpretty(trace(A)) == 'tr(𝐀)'

    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)
    C = MatrixSymbol("C", 3, 3)

    assert boldpretty(-A) == '-𝐀'
    assert boldpretty(A - A*B - B) == '-𝐁 -𝐀⋅𝐁 + 𝐀'
    assert boldpretty(-A*B - A*B*C - B) == '-𝐁 -𝐀⋅𝐁 -𝐀⋅𝐁⋅𝐂'

    A = MatrixSymbol("Addot", 3, 3)
    assert boldpretty(A) == '𝐀̈'
    omega = MatrixSymbol("omega", 3, 3)
    assert boldpretty(omega) == 'ω'
    omega = MatrixSymbol("omeganorm", 3, 3)
    assert boldpretty(omega) == '‖ω‖'

    a = Symbol('alpha')
    b = Symbol('b')
    c = MatrixSymbol("c", 3, 1)
    d = MatrixSymbol("d", 3, 1)

    assert boldpretty(a*B*c+b*d) == 'b⋅𝐝 + α⋅𝐁⋅𝐜'

    d = MatrixSymbol("delta", 3, 1)
    B = MatrixSymbol("Beta", 3, 3)

    assert boldpretty(a*B*c+b*d) == 'b⋅δ + α⋅Β⋅𝐜'

    A = MatrixSymbol("A_2", 3, 3)
    assert boldpretty(A) == '𝐀₂'

