
def test_none_kwargs():
    ax = plt.figure().subplots()
    ln, = ax.plot(range(32), linestyle=None)
    assert ln.get_linestyle() == '-'

