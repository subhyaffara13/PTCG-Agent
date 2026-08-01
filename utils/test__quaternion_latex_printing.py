
def test_Quaternion_latex_printing():
    q = Quaternion(x, y, z, t)
    assert latex(q) == r"x + y i + z j + t k"
    q = Quaternion(x, y, z, x*t)
    assert latex(q) == r"x + y i + z j + t x k"
    q = Quaternion(x, y, z, x + t)
    assert latex(q) == r"x + y i + z j + \left(t + x\right) k"

