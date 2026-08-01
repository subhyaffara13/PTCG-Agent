
def test_transform_rotates_text():
    ax = plt.gca()
    transform = mtransforms.Affine2D().rotate_deg(30)
    text = ax.text(0, 0, 'test', transform=transform,
                   transform_rotates_text=True)
    result = text.get_rotation()
    assert_almost_equal(result, 30)

