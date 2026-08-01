
def assert_func_equal(func, results, points, rtol=None, atol=None,
                      param_filter=None, knownfailure=None,
                      vectorized=True, dtype=None, nan_ok=False,
                      ignore_inf_sign=False, distinguish_nan_and_inf=True):
    if hasattr(points, 'next'):
        # it's a generator
        points = list(points)

    points = np.asarray(points)
    if points.ndim == 1:
        points = points[:,None]
    nparams = points.shape[1]

    if hasattr(results, '__name__'):
        # function
        data = points
        result_columns = None
        result_func = results
    else:
        # dataset
        data = np.c_[points, results]
        result_columns = list(range(nparams, data.shape[1]))
        result_func = None

    fdata = FuncData(func, data, list(range(nparams)),
                     result_columns=result_columns, result_func=result_func,
                     rtol=rtol, atol=atol, param_filter=param_filter,
                     knownfailure=knownfailure, nan_ok=nan_ok, vectorized=vectorized,
                     ignore_inf_sign=ignore_inf_sign,
                     distinguish_nan_and_inf=distinguish_nan_and_inf)
    fdata.check()

