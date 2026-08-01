
def test_equals_operator(idx):
    # GH9785
    assert (idx == idx).all()

