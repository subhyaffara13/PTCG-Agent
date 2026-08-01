
def test_quad_infinite_mirror():
    # Check mirrored infinite interval
    assert ae(quad(lambda x: exp(-x*x), [inf,-inf]), -sqrt(pi))
    assert ae(quad(lambda x: exp(x), [0,-inf]), -1)

