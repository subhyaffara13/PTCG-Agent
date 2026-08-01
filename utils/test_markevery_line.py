
def test_markevery_line():
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.sqrt(x/10 + 0.5)

    # check line/marker combos
    fig, ax = plt.subplots()
    ax.plot(x, y, '-o', label='default')
    ax.plot(x, y+1, '-d', markevery=None, label='mark all')
    ax.plot(x, y+2, '-s', markevery=10, label='mark every 10')
    ax.plot(x, y+3, '-+', markevery=(5, 20), label='mark every 20 starting at 5')
    ax.legend()

