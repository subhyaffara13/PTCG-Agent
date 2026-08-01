
def _get_ufuncs():
    ufuncs = []
    ufunc_names = []
    for name in sorted(sc.__dict__):
        obj = sc.__dict__[name]
        if not isinstance(obj, np.ufunc):
            continue
        msg = KNOWNFAILURES.get(obj)
        if msg is None:
            ufuncs.append(obj)
            ufunc_names.append(name)
        else:
            fail = pytest.mark.xfail(run=False, reason=msg)
            ufuncs.append(pytest.param(obj, marks=fail))
            ufunc_names.append(name)
    return ufuncs, ufunc_names

