
def test_jscode_settings():
    raises(TypeError, lambda: jscode(sin(x), method="garbage"))

