
def test_ginput(recwarn):  # recwarn undoes warn filters at exit.
    warnings.filterwarnings("ignore", "cannot show the figure")
    fig, ax = plt.subplots()
    trans = ax.transData.transform

    def single_press():
        MouseEvent("button_press_event", fig.canvas, *trans((.1, .2)), 1)._process()

    Timer(.1, single_press).start()
    assert fig.ginput() == [(.1, .2)]

    def multi_presses():
        MouseEvent("button_press_event", fig.canvas, *trans((.1, .2)), 1)._process()
        KeyEvent("key_press_event", fig.canvas, "backspace")._process()
        MouseEvent("button_press_event", fig.canvas, *trans((.3, .4)), 1)._process()
        MouseEvent("button_press_event", fig.canvas, *trans((.5, .6)), 1)._process()
        MouseEvent("button_press_event", fig.canvas, *trans((0, 0)), 2)._process()

    Timer(.1, multi_presses).start()
    np.testing.assert_allclose(fig.ginput(3), [(.3, .4), (.5, .6)])

