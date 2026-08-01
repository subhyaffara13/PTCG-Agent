
def test_gesdd_nan_error_message():
    A = np.eye(2)
    A[0, 0] = np.nan
    with pytest.raises(ValueError, match="NaN"):
        svd(A, check_finite=False)

