
def test_TR4():
    for i in [0, pi/6, pi/4, pi/3, pi/2]:
        with evaluate(False):
            eq = cos(i)
        assert isinstance(eq, cos) and TR4(eq) == cos(i)

