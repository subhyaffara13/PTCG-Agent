import re

def test_K1():
    z1, z2 = symbols('z1, z2', complex=True)
    assert re(z1 + I*z2) == -im(z2) + re(z1)
    assert im(z1 + I*z2) == im(z1) + re(z2)

