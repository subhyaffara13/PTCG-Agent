
def test_align_negative_cases(df_neg, align, exp):
    # test different align cases for all negative values
    result = df_neg.style.bar(align=align)._compute().ctx
    expected = {(0, 0): exp[0], (1, 0): exp[1], (2, 0): exp[2]}
    assert result == expected

