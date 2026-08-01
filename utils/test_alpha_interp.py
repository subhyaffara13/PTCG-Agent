
def test_alpha_interp():
    """Test the interpolation of the alpha channel on RGBA images"""
    fig, (axl, axr) = plt.subplots(1, 2)
    # full green image
    img = np.zeros((5, 5, 4))
    img[..., 1] = np.ones((5, 5))
    # transparent under main diagonal
    img[..., 3] = np.tril(np.ones((5, 5), dtype=np.uint8))
    axl.imshow(img, interpolation="none")
    axr.imshow(img, interpolation="bilinear")

