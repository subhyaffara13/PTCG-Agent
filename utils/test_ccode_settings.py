
def test_ccode_settings():
    raises(TypeError, lambda: ccode(sin(x), method="garbage"))

