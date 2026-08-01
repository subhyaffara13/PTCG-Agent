
def test_degrees():
    assert cos(0*degree) == 1
    assert cos(90*degree).ae(0)
    assert cos(180*degree).ae(-1)
    assert cos(270*degree).ae(0)
    assert cos(360*degree).ae(1)
    assert sin(0*degree) == 0
    assert sin(90*degree).ae(1)
    assert sin(180*degree).ae(0)
    assert sin(270*degree).ae(-1)
    assert sin(360*degree).ae(0)

