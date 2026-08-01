
def test_inline_function():
    from sympy.tensor import IndexedBase, Idx
    from sympy.core.symbol import symbols
    n, m = symbols('n m', integer=True)
    A, x, y = map(IndexedBase, 'Axy')
    i = Idx('i', m)
    p = FCodeGen()
    func = implemented_function('func', Lambda(n, n*(n + 1)))
    routine = make_routine('test_inline', Eq(y[i], func(x[i])))
    code = get_string(p.dump_f95, [routine])
    expected = (
        'subroutine test_inline(m, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m\n'
        'REAL*8, intent(in), dimension(1:m) :: x\n'
        'REAL*8, intent(out), dimension(1:m) :: y\n'
        'INTEGER*4 :: i\n'
        'do i = 1, m\n'
        '   y(i) = %s*%s\n'
        'end do\n'
        'end subroutine\n'
    )
    args = ('x(i)', '(x(i) + 1)')
    assert code == expected % args or\
        code == expected % args[::-1]


def test_inline_function():
    x = symbols('x')
    g = implemented_function('g', Lambda(x, 2*x))
    assert fcode(g(x)) == "      2*x"
    g = implemented_function('g', Lambda(x, 2*pi/x))
    assert fcode(g(x)) == (
        "      parameter (pi = %sd0)\n"
        "      2*pi/x"
    ) % pi.evalf(17)
    A = IndexedBase('A')
    i = Idx('i', symbols('n', integer=True))
    g = implemented_function('g', Lambda(x, x*(1 + x)*(2 + x)))
    assert fcode(g(A[i]), assign_to=A[i]) == (
        "      do i = 1, n\n"
        "         A(i) = (A(i) + 1)*(A(i) + 2)*A(i)\n"
        "      end do"
    )


def test_inline_function():
    x = symbols('x')
    g = implemented_function('g', Lambda(x, 2*x))
    assert rust_code(g(x)) == "2*x"

    g = implemented_function('g', Lambda(x, 2*x/Catalan))
    assert rust_code(g(x)) == (
        "const Catalan: f64 = %s;\n2.0*x/Catalan" % Catalan.evalf(17))

    A = IndexedBase('A')
    i = Idx('i', symbols('n', integer=True))
    g = implemented_function('g', Lambda(x, x*(1 + x)*(2 + x)))
    assert rust_code(g(A[i]), assign_to=A[i]) == (
        "for i in 0..n {\n"
        "    A[i] = (A[i] + 1)*(A[i] + 2)*A[i];\n"
        "}")

