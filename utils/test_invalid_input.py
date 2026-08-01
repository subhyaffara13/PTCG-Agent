
def test_invalid_input():
    img = np.zeros((16, 16, 4), dtype=np.uint8)

    with pytest.raises(ImageComparisonFailure,
                       match='must be 3-dimensional, but is 2-dimensional'):
        _image.calculate_rms_and_diff(img[:, :, 0], img)
    with pytest.raises(ImageComparisonFailure,
                       match='must be 3-dimensional, but is 5-dimensional'):
        _image.calculate_rms_and_diff(img, img[:, :, :, np.newaxis, np.newaxis])
    with pytest.raises(ImageComparisonFailure,
                       match='must be RGB or RGBA but has depth 2'):
        _image.calculate_rms_and_diff(img[:, :, :2], img)

    with pytest.raises(ImageComparisonFailure,
                       match=r'expected size: \(16, 16, 4\) actual size \(8, 16, 4\)'):
        _image.calculate_rms_and_diff(img, img[:8, :, :])
    with pytest.raises(ImageComparisonFailure,
                       match=r'expected size: \(16, 16, 4\) actual size \(16, 6, 4\)'):
        _image.calculate_rms_and_diff(img, img[:, :6, :])
    with pytest.raises(ImageComparisonFailure,
                       match=r'expected size: \(16, 16, 4\) actual size \(16, 16, 3\)'):
        _image.calculate_rms_and_diff(img, img[:, :, :3])

