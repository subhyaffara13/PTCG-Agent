
def test_image_array_alpha_validation():
    with pytest.raises(TypeError, match="alpha must be a float, two-d"):
        plt.imshow(np.zeros((2, 2)), alpha=[1, 1])

