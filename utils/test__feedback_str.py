
def test_Feedback_str():
    tf1 = TransferFunction(x*y**2 - z, y**3 - t**3, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(t*x**2 - t**w*x + w, t - y, y)
    assert str(Feedback(tf1*tf2, tf3)) == \
        "Feedback(Series(TransferFunction(x*y**2 - z, -t**3 + y**3, y), TransferFunction(x - y, x + y, y)), " \
        "TransferFunction(t*x**2 - t**w*x + w, t - y, y), -1)"
    assert str(Feedback(tf1, TransferFunction(1, 1, y), 1)) == \
        "Feedback(TransferFunction(x*y**2 - z, -t**3 + y**3, y), TransferFunction(1, 1, y), 1)"

