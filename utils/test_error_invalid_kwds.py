
def test_error_invalid_kwds():
    with pytest.raises(ValueError, match="Received invalid argument"):
        nx.draw(barbell, foo="bar")

