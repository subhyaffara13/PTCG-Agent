
def test_imshow_antialiased(fig_test, fig_ref,
                            img_size, fig_size, interpolation):
    np.random.seed(19680801)
    dpi = plt.rcParams["savefig.dpi"]
    A = np.random.rand(int(dpi * img_size), int(dpi * img_size))
    for fig in [fig_test, fig_ref]:
        fig.set_size_inches(fig_size, fig_size)
    ax = fig_test.subplots()
    ax.set_position([0, 0, 1, 1])
    ax.imshow(A, interpolation='auto')
    ax = fig_ref.subplots()
    ax.set_position([0, 0, 1, 1])
    ax.imshow(A, interpolation=interpolation)

