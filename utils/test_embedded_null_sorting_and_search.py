
def test_embedded_null_sorting_and_search():
    values = [
        "a\0c",
        "a\0b",
        "a",
        "\0b",
        "\0a",
        "long prefix\0c",
        "long prefix\0b",
    ]
    expected_sorted = sorted(values)

    arr = np.array(values, dtype="T")
    assert np.sort(arr).tolist() == expected_sorted
    assert arr[np.argsort(arr)].tolist() == expected_sorted
    assert np.minimum(arr[:2], arr[1::-1]).tolist() == ["a\0b", "a\0b"]
    assert np.maximum(arr[:2], arr[1::-1]).tolist() == ["a\0c", "a\0c"]

    haystack = np.array(expected_sorted, dtype="T")
    needles = ["\0b", "a\0c", "long prefix\0b"]
    expected = [bisect.bisect_left(expected_sorted, needle) for needle in needles]
    result = np.searchsorted(haystack, np.array(needles, dtype="T"))
    assert result.tolist() == expected

