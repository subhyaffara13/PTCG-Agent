
def test_sorted_results(blocks, indices, _):
    expected_result = list(map(get_index(blocks), indices))
    assert sorted_results(blocks) == expected_result

