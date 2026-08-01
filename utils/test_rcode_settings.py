
def test_rcode_settings():
    raises(TypeError, lambda: rcode(sin(x), method="garbage"))

