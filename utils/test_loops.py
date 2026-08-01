
def test_loops():
    from sympy.tensor import IndexedBase, Idx
    from sympy.core.symbol import symbols

    n, m = symbols('n,m', integer=True)
    A, x, y = map(IndexedBase, 'Axy')
    i = Idx('i', m)
    j = Idx('j', n)

    (f1, code), (f2, interface) = codegen(
        ('matrix_vector', Eq(y[i], A[i, j]*x[j])), "F95", "file", header=False, empty=False)

    assert f1 == 'file.f90'
    expected = (
        'subroutine matrix_vector(A, m, n, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m\n'
        'INTEGER*4, intent(in) :: n\n'
        'REAL*8, intent(in), dimension(1:m, 1:n) :: A\n'
        'REAL*8, intent(in), dimension(1:n) :: x\n'
        'REAL*8, intent(out), dimension(1:m) :: y\n'
        'INTEGER*4 :: i\n'
        'INTEGER*4 :: j\n'
        'do i = 1, m\n'
        '   y(i) = 0\n'
        'end do\n'
        'do i = 1, m\n'
        '   do j = 1, n\n'
        '      y(i) = %(rhs)s + y(i)\n'
        '   end do\n'
        'end do\n'
        'end subroutine\n'
    )

    assert code == expected % {'rhs': 'A(i, j)*x(j)'} or\
        code == expected % {'rhs': 'x(j)*A(i, j)'}
    assert f2 == 'file.h'
    assert interface == (
        'interface\n'
        'subroutine matrix_vector(A, m, n, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m\n'
        'INTEGER*4, intent(in) :: n\n'
        'REAL*8, intent(in), dimension(1:m, 1:n) :: A\n'
        'REAL*8, intent(in), dimension(1:n) :: x\n'
        'REAL*8, intent(out), dimension(1:m) :: y\n'
        'end subroutine\n'
        'end interface\n'
    )


def test_loops():
    n, m = symbols('n,m', integer=True)
    A = IndexedBase('A')
    x = IndexedBase('x')
    y = IndexedBase('y')
    i = Idx('i', m)
    j = Idx('j', n)

    expected = (
        'do i = 1, m\n'
        '   y(i) = 0\n'
        'end do\n'
        'do i = 1, m\n'
        '   do j = 1, n\n'
        '      y(i) = %(rhs)s\n'
        '   end do\n'
        'end do'
    )

    code = fcode(A[i, j]*x[j], assign_to=y[i], source_format='free')
    assert (code == expected % {'rhs': 'y(i) + A(i, j)*x(j)'} or
            code == expected % {'rhs': 'y(i) + x(j)*A(i, j)'} or
            code == expected % {'rhs': 'x(j)*A(i, j) + y(i)'} or
            code == expected % {'rhs': 'A(i, j)*x(j) + y(i)'})


def test_loops():
    m, n = symbols('m n', integer=True)
    A = IndexedBase('A')
    x = IndexedBase('x')
    y = IndexedBase('y')
    z = IndexedBase('z')
    i = Idx('i', m)
    j = Idx('j', n)

    assert rust_code(A[i, j]*x[j], assign_to=y[i]) == (
        "for i in 0..m {\n"
        "    y[i] = 0;\n"
        "}\n"
        "for i in 0..m {\n"
        "    for j in 0..n {\n"
        "        y[i] = A[n*i + j]*x[j] + y[i];\n"
        "    }\n"
        "}")

    assert rust_code(A[i, j]*x[j] + x[i] + z[i], assign_to=y[i]) == (
        "for i in 0..m {\n"
        "    y[i] = x[i] + z[i];\n"
        "}\n"
        "for i in 0..m {\n"
        "    for j in 0..n {\n"
        "        y[i] = A[n*i + j]*x[j] + y[i];\n"
        "    }\n"
        "}")

