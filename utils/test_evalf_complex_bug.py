
def test_evalf_complex_bug():
    assert NS('(pi+E*I)*(E+pi*I)', 15) in ('0.e-15 + 17.25866050002*I',
              '0.e-17 + 17.25866050002*I', '-0.e-17 + 17.25866050002*I')

