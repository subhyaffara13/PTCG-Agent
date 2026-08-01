
def test_get_default_filename():
    fig = plt.figure()
    assert fig.canvas.get_default_filename() == "Figure_1.png"
    fig.canvas.manager.set_window_title("0:1/2<3")
    assert fig.canvas.get_default_filename() == "0_1_2_3.png"

