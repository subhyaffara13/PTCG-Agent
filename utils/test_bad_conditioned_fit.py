
def test_bad_conditioned_fit(Poly):

    x = [0., 0., 1.]
    y = [1., 2., 3.]

    # check RankWarning is raised
    with pytest.warns(RankWarning) as record:
        Poly.fit(x, y, 2)
    assert record[0].message.args[0] == "The fit may be poorly conditioned"

