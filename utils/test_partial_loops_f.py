
def test_partial_loops_f():
    # check that loop boundaries are determined by Idx, and array strides
    # determined by shape of IndexedBase object.
    from sympy.tensor import IndexedBase, Idx
    from sympy.core.symbol import symbols
    n, m, o, p = symbols('n m o p', integer=True)
    A = IndexedBase('A', shape=(m, p))
    x = IndexedBase('x')
    y = IndexedBase('y')
    i = Idx('i', (o, m - 5))  # Note: bounds are inclusive
    j = Idx('j', n)          # dimension n corresponds to bounds (0, n - 1)

    (f1, code), (f2, interface) = codegen(
        ('matrix_vector', Eq(y[i], A[i, j]*x[j])), "F95", "file", header=False, empty=False)

    expected = (
        'subroutine matrix_vector(A, m, n, o, p, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m\n'
        'INTEGER*4, intent(in) :: n\n'
        'INTEGER*4, intent(in) :: o\n'
        'INTEGER*4, intent(in) :: p\n'
        'REAL*8, intent(in), dimension(1:m, 1:p) :: A\n'
        'REAL*8, intent(in), dimension(1:n) :: x\n'
        'REAL*8, intent(out), dimension(1:%(iup-ilow)s) :: y\n'
        'INTEGER*4 :: i\n'
        'INTEGER*4 :: j\n'
        'do i = %(ilow)s, %(iup)s\n'
        '   y(i) = 0\n'
        'end do\n'
        'do i = %(ilow)s, %(iup)s\n'
        '   do j = 1, n\n'
        '      y(i) = %(rhs)s + y(i)\n'
        '   end do\n'
        'end do\n'
        'end subroutine\n'
    ) % {
        'rhs': '%(rhs)s',
        'iup': str(m - 4),
        'ilow': str(1 + o),
        'iup-ilow': str(m - 4 - o)
    }

    assert code == expected % {'rhs': 'A(i, j)*x(j)'} or\
        code == expected % {'rhs': 'x(j)*A(i, j)'}

