
def lhs(request):
    rng = np.random.default_rng(2)
    if request.param == 0:
        return DataFrame(rng.standard_normal((10, 5)))
    elif request.param == 1:
        return Series(rng.standard_normal(5))
    elif request.param == 2:
        return Series([1, 2, np.nan, np.nan, 5])
    elif request.param == 3:
        nan_df1 = DataFrame(rng.standard_normal((10, 5)))
        nan_df1[nan_df1 > 0.5] = np.nan
        return nan_df1
    elif request.param == 4:
        return rng.standard_normal()
    else:
        raise ValueError(f"{request.param}")

