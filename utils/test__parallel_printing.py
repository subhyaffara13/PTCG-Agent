
def test_Parallel_printing():
    tf1 = TransferFunction(x*y**2 - z, y**3 - t**3, y)
    tf2 = TransferFunction(x - y, x + y, y)
    assert latex(Parallel(tf1, tf2)) == \
        r'\frac{x y^{2} - z}{- t^{3} + y^{3}} + \frac{x - y}{x + y}'
    assert latex(Parallel(-tf2, tf1)) == \
        r'\frac{- x + y}{x + y} + \frac{x y^{2} - z}{- t^{3} + y^{3}}'

    M_1 = Matrix([[5, 6], [6, 5/s]])
    T_1 = TransferFunctionMatrix.from_Matrix(M_1, s)
    M_2 = Matrix([[5/s, 6], [6, 5/(s - 1)]])
    T_2 = TransferFunctionMatrix.from_Matrix(M_2, s)
    M_3 = Matrix([[6, 5/(s*(s - 1))], [5, 6]])
    T_3 = TransferFunctionMatrix.from_Matrix(M_3, s)
    assert latex(T_1 + T_2 + T_3) == r'\left[\begin{matrix}\frac{5}{1} & \frac{6}{1}\\\frac{6}{1} & \frac{5}{s}\end{matrix}\right]' \
        r'_\tau + \left[\begin{matrix}\frac{5}{s} & \frac{6}{1}\\\frac{6}{1} & \frac{5}{s - 1}\end{matrix}\right]_\tau + \left[\begin{matrix}' \
            r'\frac{6}{1} & \frac{5}{s \left(s - 1\right)}\\\frac{5}{1} & \frac{6}{1}\end{matrix}\right]_\tau' \
                == latex(MIMOParallel(T_1, T_2, T_3)) == latex(MIMOParallel(T_1, MIMOParallel(T_2, T_3))) == latex(MIMOParallel(MIMOParallel(T_1, T_2), T_3))

