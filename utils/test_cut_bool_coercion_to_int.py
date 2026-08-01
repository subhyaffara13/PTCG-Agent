
def test_cut_bool_coercion_to_int(bins, box, compare):
    # issue 20303
    data_expected = box([0, 1, 1, 0, 1] * 10)
    data_result = box([False, True, True, False, True] * 10)
    expected = cut(data_expected, bins, duplicates="drop")
    result = cut(data_result, bins, duplicates="drop")
    compare(result, expected)

