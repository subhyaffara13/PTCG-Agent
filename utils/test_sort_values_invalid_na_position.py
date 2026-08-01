
def test_sort_values_invalid_na_position(index_with_missing, na_position):
    with pytest.raises(ValueError, match=f"invalid na_position: {na_position}"):
        index_with_missing.sort_values(na_position=na_position)

