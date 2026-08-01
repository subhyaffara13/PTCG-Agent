
def test_ncf_cdf_spotcheck():
    # Regression test for gh-15582 testing against values from R/MATLAB
    # Generate check_val from R or MATLAB as follows:
    #          R: pf(20, df1 = 6, df2 = 33, ncp = 30.4) = 0.998921
    #     MATLAB: ncfcdf(20, 6, 33, 30.4) = 0.998921
    scipy_val = stats.ncf.cdf(20, 6, 33, 30.4)
    check_val = 0.998921
    assert_allclose(check_val, np.round(scipy_val, decimals=6))

