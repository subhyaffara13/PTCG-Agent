
def test_TransferFunctionMatrix_printing():
    tf1 = TransferFunction(p, p + x, p)
    tf2 = TransferFunction(-s + p, p + s, p)
    tf3 = TransferFunction(p, y**2 + 2*y + 3, p)
    assert latex(TransferFunctionMatrix([[tf1], [tf2]])) == \
        r'\left[\begin{matrix}\frac{p}{p + x}\\\frac{p - s}{p + s}\end{matrix}\right]_\tau'
    assert latex(TransferFunctionMatrix([[tf1, tf2], [tf3, -tf1]])) == \
        r'\left[\begin{matrix}\frac{p}{p + x} & \frac{p - s}{p + s}\\\frac{p}{y^{2} + 2 y + 3} & \frac{\left(-1\right) p}{p + x}\end{matrix}\right]_\tau'

