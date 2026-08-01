
def assert_fit_warnings(dist):
    param = ['floc', 'fscale']
    if dist.shapes:
        nshapes = len(dist.shapes.split(","))
        param += ['f0', 'f1', 'f2'][:nshapes]
    all_fixed = dict(zip(param, np.arange(len(param))))
    data = [1, 2, 3]
    with pytest.raises(RuntimeError,
                       match="All parameters fixed. There is nothing "
                       "to optimize."):
        dist.fit(data, **all_fixed)
    with pytest.raises(ValueError,
                       match="The data contains non-finite values"):
        dist.fit([np.nan])
    with pytest.raises(ValueError,
                       match="The data contains non-finite values"):
        dist.fit([np.inf])
    with pytest.raises(TypeError, match="Unknown keyword arguments:"):
        dist.fit(data, extra_keyword=2)
    with pytest.raises(TypeError, match="Too many positional arguments."):
        dist.fit(data, *[1]*(len(param) - 1))

