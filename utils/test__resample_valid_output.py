import functools

def test__resample_valid_output():
    resample = functools.partial(mpl._image.resample, transform=Affine2D())
    with pytest.raises(TypeError, match="incompatible function arguments"):
        resample(np.zeros((9, 9)), None)
    with pytest.raises(ValueError, match="different dimensionalities"):
        resample(np.zeros((9, 9)), np.zeros((9, 9, 4)))
    with pytest.raises(ValueError, match="different dimensionalities"):
        resample(np.zeros((9, 9, 4)), np.zeros((9, 9)))
    with pytest.raises(ValueError, match="3D input array must be RGBA"):
        resample(np.zeros((9, 9, 3)), np.zeros((9, 9, 4)))
    with pytest.raises(ValueError, match="3D output array must be RGBA"):
        resample(np.zeros((9, 9, 4)), np.zeros((9, 9, 3)))
    with pytest.raises(ValueError, match="mismatched types"):
        resample(np.zeros((9, 9), np.uint8), np.zeros((9, 9)))
    with pytest.raises(ValueError, match="must be C-contiguous"):
        resample(np.zeros((9, 9)), np.zeros((9, 9)).T)

    out = np.zeros((9, 9))
    out.flags.writeable = False
    with pytest.raises(ValueError, match="Output array must be writeable"):
        resample(np.zeros((9, 9)), out)

