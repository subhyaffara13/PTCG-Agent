
def test_overflow():
    x = np.array([1.0, 2.0, 3.0, 2.0e5])
    y = np.arange(len(x))

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlim(2, 6)

