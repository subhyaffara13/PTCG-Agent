
def test_evalf_basic():
    assert NS('pi', 15) == '3.14159265358979'
    assert NS('2/3', 10) == '0.6666666667'
    assert NS('355/113-pi', 6) == '2.66764e-7'
    assert NS('16*atan(1/5)-4*atan(1/239)', 15) == '3.14159265358979'

