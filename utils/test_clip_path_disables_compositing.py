
def test_clip_path_disables_compositing(fig_test, fig_ref):
    t = np.arange(9).reshape((3, 3))
    for fig in [fig_test, fig_ref]:
        ax = fig.add_subplot()
        ax.imshow(t, clip_path=(mpl.path.Path([(0, 0), (0, 1), (1, 0)]),
                                ax.transData))
        ax.imshow(t, clip_path=(mpl.path.Path([(1, 1), (1, 2), (2, 1)]),
                                ax.transData))
    fig_ref.suppressComposite = True

