
def test_expanding_consistency_var_debiasing_factors(all_data, min_periods):
    # check variance debiasing factors
    var_unbiased_x = all_data.expanding(min_periods=min_periods).var()
    var_biased_x = all_data.expanding(min_periods=min_periods).var(ddof=0)
    var_debiasing_factors_x = all_data.expanding().count() / (
        all_data.expanding().count() - 1.0
    ).replace(0.0, np.nan)
    tm.assert_equal(var_unbiased_x, var_biased_x * var_debiasing_factors_x)

