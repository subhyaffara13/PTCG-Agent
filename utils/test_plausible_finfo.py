
def test_plausible_finfo():
    # Assert that finfo returns reasonable results for all types
    for ftype in np._core.sctypes['float'] + np._core.sctypes['complex']:
        info = np.finfo(ftype)
        assert_(info.nmant > 1)
        assert_(info.minexp < -1)
        assert_(info.maxexp > 1)

