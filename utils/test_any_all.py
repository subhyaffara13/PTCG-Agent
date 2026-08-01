
def test_any_all(
    values, exp_any, exp_all, exp_any_noskip, exp_all_noskip, using_python_scalars, con
):
    # the methods return numpy scalars
    if not using_python_scalars or con is pd.array:
        exp_any = pd.NA if exp_any is pd.NA else np.bool_(exp_any)
        exp_all = pd.NA if exp_all is pd.NA else np.bool_(exp_all)
        exp_any_noskip = pd.NA if exp_any_noskip is pd.NA else np.bool_(exp_any_noskip)
        exp_all_noskip = pd.NA if exp_all_noskip is pd.NA else np.bool_(exp_all_noskip)

    a = con(values, dtype="boolean")
    assert a.any() is exp_any
    assert a.all() is exp_all
    assert a.any(skipna=False) is exp_any_noskip
    assert a.all(skipna=False) is exp_all_noskip

