import os

def test_imread_pil_uint16():
    img = plt.imread(os.path.join(os.path.dirname(__file__),
                     'baseline_images', 'test_image', 'uint16.tif'))
    assert img.dtype == np.uint16
    assert np.sum(img) == 134184960

