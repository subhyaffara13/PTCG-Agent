
def test_errorbar_remove():
    x = np.arange(5)
    y = np.arange(5)

    fig, ax = plt.subplots()
    ec = ax.errorbar(x, y, xerr=1, yerr=1)

    assert len(ax.containers) == 1
    assert len(ax.lines) == 5
    assert len(ax.collections) == 2

    ec.remove()

    assert not ax.containers
    assert not ax.lines
    assert not ax.collections


def test_errorbar_remove():

    # Regression test for a bug that caused remove to fail when using
    # fmt='none'

    ax = plt.gca()

    eb = ax.errorbar([1], [1])
    eb.remove()

    eb = ax.errorbar([1], [1], xerr=1)
    eb.remove()

    eb = ax.errorbar([1], [1], yerr=2)
    eb.remove()

    eb = ax.errorbar([1], [1], xerr=[2], yerr=2)
    eb.remove()

    eb = ax.errorbar([1], [1], fmt='none')
    eb.remove()

