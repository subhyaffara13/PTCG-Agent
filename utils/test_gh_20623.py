
def test_gh_20623(diagram_type):
    rng = np.random.default_rng(123)
    invalid_data = rng.random((4, 10, 3))
    with pytest.raises(ValueError, match="dimensions"):
        diagram_type(invalid_data)

