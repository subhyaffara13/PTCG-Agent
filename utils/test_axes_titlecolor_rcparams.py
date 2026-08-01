
def test_axes_titlecolor_rcparams():
    mpl.rcParams['axes.titlecolor'] = 'r'
    _, ax = plt.subplots()
    title = ax.set_title("Title")
    assert title.get_color() == 'r'

