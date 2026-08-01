
def test_no_subslice_with_transform(fig_ref, fig_test):
    ax = fig_ref.add_subplot()
    x = np.arange(2000)
    ax.plot(x + 2000, x)

    ax = fig_test.add_subplot()
    t = mtransforms.Affine2D().translate(2000.0, 0.0)
    ax.plot(x, x, transform=t+ax.transData)

