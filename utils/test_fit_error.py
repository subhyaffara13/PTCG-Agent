
def test_fit_error():
    data = np.concatenate([np.zeros(29), np.ones(21)])
    message = "Optimization converged to parameters that are..."
    with pytest.raises(FitError, match=message), \
            pytest.warns(RuntimeWarning):
        stats.beta.fit(data)

