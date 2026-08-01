
def test_polar_log():
    fig = plt.figure()
    ax = fig.add_subplot(polar=True)

    ax.set_rscale('log')
    ax.set_rlim(1, 1000)

    n = 100
    ax.plot(np.linspace(0, 2 * np.pi, n), np.logspace(0, 2, n))

