import itertools

def test_ft2image_draw_rect_filled():
    width = 23
    height = 42
    for x0, y0, x1, y1 in itertools.product([1, 100], [2, 200], [4, 400], [8, 800]):
        with pytest.warns(mpl.MatplotlibDeprecationWarning):
            im = ft2font.FT2Image(width, height)
        im.draw_rect_filled(x0, y0, x1, y1)
        a = np.asarray(im)
        assert a.dtype == np.uint8
        assert a.shape == (height, width)
        if x0 == 100 or y0 == 200:
            # All the out-of-bounds starts should get automatically clipped.
            assert np.sum(a) == 0
        else:
            # Otherwise, ends are clipped to the dimension, but are also _inclusive_.
            filled = (min(x1 + 1, width) - x0) * (min(y1 + 1, height) - y0)
            assert np.sum(a) == 255 * filled

