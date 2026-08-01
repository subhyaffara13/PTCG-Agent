
def test_str_cat(index_or_series, infer_string):
    with option_context("future.infer_string", infer_string):
        box = index_or_series
        # test_cat above tests "str_cat" from ndarray;
        # here testing "str.cat" from Series/Index to ndarray/list
        s = box(["a", "a", "b", "b", "c", np.nan])

        # single array
        result = s.str.cat()
        expected = "aabbc"
        assert result == expected

        result = s.str.cat(na_rep="-")
        expected = "aabbc-"
        assert result == expected

        result = s.str.cat(sep="_", na_rep="NA")
        expected = "a_a_b_b_c_NA"
        assert result == expected

        t = np.array(["a", np.nan, "b", "d", "foo", np.nan], dtype=object)
        expected = box(["aa", "a-", "bb", "bd", "cfoo", "--"])

        # Series/Index with array
        result = s.str.cat(t, na_rep="-")
        tm.assert_equal(result, expected)

        # Series/Index with list
        result = s.str.cat(list(t), na_rep="-")
        tm.assert_equal(result, expected)

        # errors for incorrect lengths
        rgx = r"If `others` contains arrays or lists \(or other list-likes.*"
        z = Series(["1", "2", "3"])

        with pytest.raises(ValueError, match=rgx):
            s.str.cat(z.values)

        with pytest.raises(ValueError, match=rgx):
            s.str.cat(list(z))

