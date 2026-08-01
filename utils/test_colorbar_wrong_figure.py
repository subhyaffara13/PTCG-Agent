
def test_colorbar_wrong_figure():
    # If we decide in the future to disallow calling colorbar() on the "wrong" figure,
    # just delete this test.
    fig_tl = plt.figure(layout="tight")
    fig_cl = plt.figure(layout="constrained")
    im = fig_cl.add_subplot().imshow([[0, 1]])
    # Make sure this doesn't try to setup a gridspec-controlled colorbar on fig_cl,
    # which would crash CL.
    with pytest.warns(UserWarning, match="different Figure"):
        fig_tl.colorbar(im)
    fig_tl.draw_without_rendering()
    fig_cl.draw_without_rendering()

