
def test_mathtext_cmr10_minus_sign():
    # cmr10 does not contain a minus sign and used to issue a warning
    # RuntimeWarning: Glyph 8722 missing from current font.
    mpl.rcParams['font.family'] = 'cmr10'
    mpl.rcParams['axes.formatter.use_mathtext'] = True
    fig, ax = plt.subplots()
    ax.plot(range(-1, 1), range(-1, 1))
    # draw to make sure we have no warnings
    fig.canvas.draw()

