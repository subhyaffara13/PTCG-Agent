
def test_dummy_loops_f95():
    from sympy.tensor import IndexedBase, Idx
    i, m = symbols('i m', integer=True, cls=Dummy)
    x = IndexedBase('x')
    y = IndexedBase('y')
    i = Idx(i, m)
    expected = (
        'subroutine test_dummies(m_%(mcount)i, x, y)\n'
        'implicit none\n'
        'INTEGER*4, intent(in) :: m_%(mcount)i\n'
        'REAL*8, intent(in), dimension(1:m_%(mcount)i) :: x\n'
        'REAL*8, intent(out), dimension(1:m_%(mcount)i) :: y\n'
        'INTEGER*4 :: i_%(icount)i\n'
        'do i_%(icount)i = 1, m_%(mcount)i\n'
        '   y(i_%(icount)i) = x(i_%(icount)i)\n'
        'end do\n'
        'end subroutine\n'
    ) % {'icount': i.label.dummy_index, 'mcount': m.dummy_index}
    r = make_routine('test_dummies', Eq(y[i], x[i]))
    c = FCodeGen()
    code = get_string(c.dump_f95, [r])
    assert code == expected

