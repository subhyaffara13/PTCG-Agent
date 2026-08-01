
def test_format_approx():
    f = cbook._format_approx
    assert f(0, 1) == '0'
    assert f(0, 2) == '0'
    assert f(0, 3) == '0'
    assert f(-0.0123, 1) == '-0'
    assert f(1e-7, 5) == '0'
    assert f(0.0012345600001, 5) == '0.00123'
    assert f(-0.0012345600001, 5) == '-0.00123'
    assert f(0.0012345600001, 8) == f(0.0012345600001, 10) == '0.00123456'

