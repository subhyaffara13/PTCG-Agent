
def test_opportunistic_simplification():
    # this test relates to issue #10718, #9480, #11434

    # issue #9480
    m = Matrix([[-5 + 5*sqrt(2), -5], [-5*sqrt(2)/2 + 5, -5*sqrt(2)/2]])
    assert m.rank() == 1

    # issue #10781
    m = Matrix([[3+3*sqrt(3)*I, -9],[4,-3+3*sqrt(3)*I]])
    assert simplify(m.rref()[0] - Matrix([[1, -9/(3 + 3*sqrt(3)*I)], [0, 0]])) == zeros(2, 2)

    # issue #11434
    ax,ay,bx,by,cx,cy,dx,dy,ex,ey,t0,t1 = symbols('a_x a_y b_x b_y c_x c_y d_x d_y e_x e_y t_0 t_1')
    m = Matrix([[ax,ay,ax*t0,ay*t0,0],[bx,by,bx*t0,by*t0,0],[cx,cy,cx*t0,cy*t0,1],[dx,dy,dx*t0,dy*t0,1],[ex,ey,2*ex*t1-ex*t0,2*ey*t1-ey*t0,0]])
    assert m.rank() == 4


def test_opportunistic_simplification():
    # this test relates to issue #10718, #9480, #11434

    # issue #9480
    m = Matrix([[-5 + 5*sqrt(2), -5], [-5*sqrt(2)/2 + 5, -5*sqrt(2)/2]])
    assert m.rank() == 1

    # issue #10781
    m = Matrix([[3+3*sqrt(3)*I, -9],[4,-3+3*sqrt(3)*I]])
    assert simplify(m.rref()[0] - Matrix([[1, -9/(3 + 3*sqrt(3)*I)], [0, 0]])) == zeros(2, 2)

    # issue #11434
    ax,ay,bx,by,cx,cy,dx,dy,ex,ey,t0,t1 = symbols('a_x a_y b_x b_y c_x c_y d_x d_y e_x e_y t_0 t_1')
    m = Matrix([[ax,ay,ax*t0,ay*t0,0],[bx,by,bx*t0,by*t0,0],[cx,cy,cx*t0,cy*t0,1],[dx,dy,dx*t0,dy*t0,1],[ex,ey,2*ex*t1-ex*t0,2*ey*t1-ey*t0,0]])
    assert m.rank() == 4

