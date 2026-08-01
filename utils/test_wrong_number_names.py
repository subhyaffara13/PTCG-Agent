
def test_wrong_number_names(index):
    names = index.nlevels * ["apple", "banana", "carrot"]
    with pytest.raises(ValueError, match="^Length"):
        index.names = names

