
def test_framealpha():
    x = np.linspace(1, 100, 100)
    y = x
    plt.plot(x, y, label='mylabel', lw=10)
    plt.legend(framealpha=0.5, loc='upper right')

