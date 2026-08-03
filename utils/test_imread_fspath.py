from pathlib import Path


def test_imread_fspath():
    img = plt.imread(
        Path(__file__).parent / 'baseline_images/test_image/uint16.tif')
    assert img.dtype == np.uint16
    assert np.sum(img) == 134184960

