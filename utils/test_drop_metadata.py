
def test_drop_metadata():
    def _compare_dtypes(dt1, dt2):
        return np.can_cast(dt1, dt2, casting='no')

    # structured dtype
    dt = np.dtype([('l1', [('l2', np.dtype('S8', metadata={'msg': 'toto'}))])],
                  metadata={'msg': 'titi'})
    dt_m = _utils_impl.drop_metadata(dt)
    assert _compare_dtypes(dt, dt_m) is True
    assert dt_m.metadata is None
    assert dt_m['l1'].metadata is None
    assert dt_m['l1']['l2'].metadata is None

    # alignment
    dt = np.dtype([('x', '<f8'), ('y', '<i4')],
                  align=True,
                  metadata={'msg': 'toto'})
    dt_m = _utils_impl.drop_metadata(dt)
    assert _compare_dtypes(dt, dt_m) is True
    assert dt_m.metadata is None

    # subdtype
    dt = np.dtype('8f',
                  metadata={'msg': 'toto'})
    dt_m = _utils_impl.drop_metadata(dt)
    assert _compare_dtypes(dt, dt_m) is True
    assert dt_m.metadata is None

    # scalar
    dt = np.dtype('uint32',
                  metadata={'msg': 'toto'})
    dt_m = _utils_impl.drop_metadata(dt)
    assert _compare_dtypes(dt, dt_m) is True
    assert dt_m.metadata is None

