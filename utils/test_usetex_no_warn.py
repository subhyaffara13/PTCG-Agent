
def test_usetex_no_warn(caplog):
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.serif'] = 'Computer Modern'
    mpl.rcParams['text.usetex'] = True

    fig, ax = plt.subplots()
    ax.plot(0, 0, label='input')
    ax.legend(title="My legend")

    fig.canvas.draw()
    assert "Font family ['serif'] not found." not in caplog.text

