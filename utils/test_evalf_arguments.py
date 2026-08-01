
def test_evalf_arguments():
    raises(TypeError, lambda: pi.evalf(method="garbage"))

