
def test_DifferentialExtension_equality():
    DE1 = DE2 = DifferentialExtension(log(x), x)
    assert DE1 == DE2

