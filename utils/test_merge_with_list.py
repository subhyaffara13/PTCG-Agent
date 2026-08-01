
def test_merge_with_list():
    assert merge_with(sum, [{'a': 1}, {'a': 2}]) == {'a': 3}

