
def test_matshow(fig_test, fig_ref):
    mpl.style.use("mpl20")
    a = np.random.rand(32, 32)
    fig_test.add_subplot().matshow(a)
    ax_ref = fig_ref.add_subplot()
    ax_ref.imshow(a)
    ax_ref.xaxis.tick_top()
    ax_ref.xaxis.set_ticks_position('both')


def test_matshow():
    fig = plt.figure()
    arr = [[0, 1], [1, 2]]

    # Smoke test that matshow does not ask for a new figsize on the existing figure
    plt.matshow(arr, fignum=fig.number)

