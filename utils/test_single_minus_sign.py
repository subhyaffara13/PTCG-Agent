
def test_single_minus_sign():
    fig = plt.figure()
    fig.text(0.5, 0.5, '$-$')
    fig.canvas.draw()
    t = np.asarray(fig.canvas.renderer.buffer_rgba())
    assert (t != 0xff).any()  # assert that canvas is not all white.

