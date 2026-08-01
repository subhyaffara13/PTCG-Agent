
def test_scale_swapping(fig_test, fig_ref):
    np.random.seed(19680801)
    samples = np.random.normal(size=10)
    x = np.linspace(-5, 5, 10)

    for fig, log_state in zip([fig_test, fig_ref], [True, False]):
        ax = fig.subplots()
        ax.hist(samples, log=log_state, density=True)
        ax.plot(x, np.exp(-(x**2) / 2) / np.sqrt(2 * np.pi))
        fig.canvas.draw()
        ax.set_yscale('linear')

