
def test_multivar_resample():
    cmap = mpl.multivar_colormaps['3VarAddA']
    cmap_resampled = cmap.resampled((None, 10, 3))

    assert_allclose(cmap_resampled[1](0.25), (0.093, 0.116, 0.059, 1.0))
    assert_allclose(cmap_resampled((0, 0.25, 0)), (0.093, 0.116, 0.059, 1.0))
    assert_allclose(cmap_resampled((1, 0.25, 1)), (0.417271, 0.264624, 0.274976, 1.),
                                   atol=0.01)

    with pytest.raises(ValueError, match="lutshape must be of length"):
        cmap = cmap.resampled(4)

