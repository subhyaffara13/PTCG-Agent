
def test_P33():
    w, t = symbols('w t')
    M = Matrix([[0,    1,      0,   0],
                [0,    0,      0, 2*w],
                [0,    0,      0,   1],
                [0, -2*w, 3*w**2,   0]])
    assert exp(M*t).rewrite(cos).expand() == Matrix([
        [1, -3*t + 4*sin(t*w)/w,  6*t*w - 6*sin(t*w), -2*cos(t*w)/w + 2/w],
        [0,      4*cos(t*w) - 3, -6*w*cos(t*w) + 6*w,          2*sin(t*w)],
        [0,  2*cos(t*w)/w - 2/w,     -3*cos(t*w) + 4,          sin(t*w)/w],
        [0,         -2*sin(t*w),        3*w*sin(t*w),            cos(t*w)]])

