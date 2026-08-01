
def test_gh_22250(filter_size, exp):
    rng = np.random.default_rng(42)
    image = np.zeros((20,))
    noisy_image = image + 0.4 * rng.random(image.shape)
    result = ndimage.median_filter(noisy_image, size=filter_size, mode='wrap')
    assert_allclose(result, exp)

