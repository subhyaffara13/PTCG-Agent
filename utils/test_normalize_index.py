
def test_normalize_index():
    idx = Index(["ＡＢＣ", "１２３", "ｱｲｴ"])  # noqa: RUF001
    expected = Index(["ABC", "123", "アイエ"])
    result = idx.str.normalize("NFKC")
    tm.assert_index_equal(result, expected)

