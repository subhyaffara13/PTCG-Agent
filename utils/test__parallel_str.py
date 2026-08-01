
def test_Parallel_str():
    tf1 = TransferFunction(x*y**2 - z, y**3 - t**3, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(t*x**2 - t**w*x + w, t - y, y)
    assert str(Parallel(tf1, tf2)) == \
        "Parallel(TransferFunction(x*y**2 - z, -t**3 + y**3, y), TransferFunction(x - y, x + y, y))"
    assert str(Parallel(tf1, tf2, tf3)) == \
        "Parallel(TransferFunction(x*y**2 - z, -t**3 + y**3, y), TransferFunction(x - y, x + y, y), TransferFunction(t*x**2 - t**w*x + w, t - y, y))"
    assert str(Parallel(-tf2, tf1)) == \
        "Parallel(TransferFunction(-x + y, x + y, y), TransferFunction(x*y**2 - z, -t**3 + y**3, y))"

