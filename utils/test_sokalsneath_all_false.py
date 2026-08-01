
def test_sokalsneath_all_false():
    # Regression test for ticket #876
    with pytest.raises(ValueError):
        sokalsneath([False, False, False], [False, False, False])

