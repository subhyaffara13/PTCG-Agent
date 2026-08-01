
def test_deterimant():
    assert ImmutableMatrix(4, 4, lambda i, j: i + j).det() == 0

