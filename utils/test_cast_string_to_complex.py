
def test_cast_string_to_complex():
    # GH 4895
    expected = pd.DataFrame(["1.0+5j", "1.5-3j"], dtype=complex)
    result = pd.DataFrame(["1.0+5j", "1.5-3j"]).astype(complex)
    tm.assert_frame_equal(result, expected)

