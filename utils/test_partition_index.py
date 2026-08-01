
def test_partition_index(method, exp):
    # https://github.com/pandas-dev/pandas/issues/23558

    values = Index(["a_b_c", "c_d_e", "f_g_h", np.nan, None])

    result = getattr(values.str, method)("_", expand=False)
    exp = Index(np.array(exp, dtype=object), dtype=object)
    tm.assert_index_equal(result, exp)
    assert result.nlevels == 1

