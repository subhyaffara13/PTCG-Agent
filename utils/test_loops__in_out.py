
def test_loops_InOut():
    from sympy.tensor import IndexedBase, Idx
    from sympy.core.symbol import symbols

    i, j, n, m = symbols('i,j,n,m', integer=True)
    A, x, y = symbols('A,x,y')
    A = IndexedBase(A)[Idx(i, m), Idx(j, n)]
    x = IndexedBase(x)[Idx(j, n)]
    y = IndexedBase(y)[Idx(i, m)]

    (f1, code), (f2, interface) = codegen(
        ('matrix_vector', Eq(y, y + A*x)), "F95", "file", header=False, empty=False)

    assert f1 == 'file.f90'
    expected = (
        'subroutine matrix_vector(A, m, n, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m\n'
        'INTEGER*4, intent(in) :: n\n'
        'REAL*8, intent(in), dimension(1:m, 1:n) :: A\n'
        'REAL*8, intent(in), dimension(1:n) :: x\n'
        'REAL*8, intent(inout), dimension(1:m) :: y\n'
        'INTEGER*4 :: i\n'
        'INTEGER*4 :: j\n'
        'do i = 1, m\n'
        '   do j = 1, n\n'
        '      y(i) = %(rhs)s + y(i)\n'
        '   end do\n'
        'end do\n'
        'end subroutine\n'
    )

    assert (code == expected % {'rhs': 'A(i, j)*x(j)'} or
            code == expected % {'rhs': 'x(j)*A(i, j)'})
    assert f2 == 'file.h'
    assert interface == (
        'interface\n'
        'subroutine matrix_vector(A, m, n, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m\n'
        'INTEGER*4, intent(in) :: n\n'
        'REAL*8, intent(in), dimension(1:m, 1:n) :: A\n'
        'REAL*8, intent(in), dimension(1:n) :: x\n'
        'REAL*8, intent(inout), dimension(1:m) :: y\n'
        'end subroutine\n'
        'end interface\n'
    )

