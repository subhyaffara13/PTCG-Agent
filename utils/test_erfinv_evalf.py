
def test_erfinv_evalf():
    assert abs( erfinv(Float(0.2)) - 0.179143454621292 ) < 1E-13

