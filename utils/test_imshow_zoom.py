
def test_imshow_zoom(fig_test, fig_ref):
    # should be less than 3 upsample, so should be nearest...
    np.random.seed(19680801)
    dpi = plt.rcParams["savefig.dpi"]
    A = np.random.rand(int(dpi * 3), int(dpi * 3))
    for fig in [fig_test, fig_ref]:
        fig.set_size_inches(2.9, 2.9)
    ax = fig_test.subplots()
    ax.imshow(A, interpolation='auto')
    ax.set_xlim(10, 20)
    ax.set_ylim(10, 20)
    ax = fig_ref.subplots()
    ax.imshow(A, interpolation='nearest')
    ax.set_xlim(10, 20)
    ax.set_ylim(10, 20)

