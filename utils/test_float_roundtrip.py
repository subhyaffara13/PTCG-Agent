
def test_float_roundtrip():
    x = sympify(0.8975979010256552)
    y = float(mp.doprint(x).strip('</cn>'))
    assert x == y

