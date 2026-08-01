
def test_Series_printing():
    tf1 = TransferFunction(x*y**2 - z, y**3 - t**3, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(t*x**2 - t**w*x + w, t - y, y)
    assert latex(Series(tf1, tf2)) == \
        r'\left(\frac{x y^{2} - z}{- t^{3} + y^{3}}\right) \left(\frac{x - y}{x + y}\right)'
    assert latex(Series(tf1, tf2, tf3)) == \
        r'\left(\frac{x y^{2} - z}{- t^{3} + y^{3}}\right) \left(\frac{x - y}{x + y}\right) \left(\frac{t x^{2} - t^{w} x + w}{t - y}\right)'
    assert latex(Series(-tf2, tf1)) == \
        r'\left(\frac{- x + y}{x + y}\right) \left(\frac{x y^{2} - z}{- t^{3} + y^{3}}\right)'

    M_1 = Matrix([[5/s], [5/(2*s)]])
    T_1 = TransferFunctionMatrix.from_Matrix(M_1, s)
    M_2 = Matrix([[5, 6*s**3]])
    T_2 = TransferFunctionMatrix.from_Matrix(M_2, s)
    # Brackets
    assert latex(T_1*(T_2 + T_2)) == \
        r'\left[\begin{matrix}\frac{5}{s}\\\frac{5}{2 s}\end{matrix}\right]_\tau\cdot\left(\left[\begin{matrix}\frac{5}{1} &' \
        r' \frac{6 s^{3}}{1}\end{matrix}\right]_\tau + \left[\begin{matrix}\frac{5}{1} & \frac{6 s^{3}}{1}\end{matrix}\right]_\tau\right)' \
            == latex(MIMOSeries(MIMOParallel(T_2, T_2), T_1))
    # No Brackets
    M_3 = Matrix([[5, 6], [6, 5/s]])
    T_3 = TransferFunctionMatrix.from_Matrix(M_3, s)
    assert latex(T_1*T_2 + T_3) == r'\left[\begin{matrix}\frac{5}{s}\\\frac{5}{2 s}\end{matrix}\right]_\tau\cdot\left[\begin{matrix}' \
        r'\frac{5}{1} & \frac{6 s^{3}}{1}\end{matrix}\right]_\tau + \left[\begin{matrix}\frac{5}{1} & \frac{6}{1}\\\frac{6}{1} & ' \
            r'\frac{5}{s}\end{matrix}\right]_\tau' == latex(MIMOParallel(MIMOSeries(T_2, T_1), T_3))

