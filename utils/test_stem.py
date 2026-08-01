
def test_stem(text_placeholders):
    x = np.linspace(0.1, 2 * np.pi, 100)

    fig, ax = plt.subplots()
    ax.stem(x, np.cos(x),
            linefmt='C2-.', markerfmt='k+', basefmt='C1-.', label='stem')
    ax.legend()

