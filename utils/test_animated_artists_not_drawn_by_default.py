
def test_animated_artists_not_drawn_by_default():
    fig, (ax1, ax2) = plt.subplots(ncols=2)

    imdata = np.random.random((20, 20))
    lndata = imdata[0]

    im = ax1.imshow(imdata, animated=True)
    (ln,) = ax2.plot(lndata, animated=True)

    with (unittest.mock.patch.object(im, "draw", name="im.draw") as mocked_im_draw,
          unittest.mock.patch.object(ln, "draw", name="ln.draw") as mocked_ln_draw):
        fig.draw_without_rendering()

    mocked_im_draw.assert_not_called()
    mocked_ln_draw.assert_not_called()

