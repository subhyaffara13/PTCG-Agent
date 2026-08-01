
def test_errorbar_colorcycle():

    f, ax = plt.subplots()
    x = np.arange(10)
    y = 2*x

    e1, _, _ = ax.errorbar(x, y, c=None)
    e2, _, _ = ax.errorbar(x, 2*y, c=None)
    ln1, = ax.plot(x, 4*y)

    assert mcolors.to_rgba(e1.get_color()) == mcolors.to_rgba('C0')
    assert mcolors.to_rgba(e2.get_color()) == mcolors.to_rgba('C1')
    assert mcolors.to_rgba(ln1.get_color()) == mcolors.to_rgba('C2')

