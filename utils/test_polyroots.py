
def test_polyroots():
    p = polyroots([1,-4])
    assert p[0].ae(4)
    p, q = polyroots([1,2,3])
    assert p.ae(-1 - sqrt(2)*j)
    assert q.ae(-1 + sqrt(2)*j)
    #this is not a real test, it only tests a specific case
    assert polyroots([1]) == []
    pytest.raises(ValueError, lambda: polyroots([0]))

