
def test_stackplot_baseline():
    np.random.seed(0)

    def layers(n, m):
        a = np.zeros((m, n))
        for i in range(n):
            for j in range(5):
                x = 1 / (.1 + np.random.random())
                y = 2 * np.random.random() - .5
                z = 10 / (.1 + np.random.random())
                a[:, i] += x * np.exp(-((np.arange(m) / m - y) * z) ** 2)
        return a

    d = layers(3, 100)
    d[50, :] = 0  # test for fixed weighted wiggle (issue #6313)

    fig, axs = plt.subplots(2, 2)

    axs[0, 0].stackplot(range(100), d.T, baseline='zero')
    axs[0, 1].stackplot(range(100), d.T, baseline='sym')
    axs[1, 0].stackplot(range(100), d.T, baseline='wiggle')
    axs[1, 1].stackplot(range(100), d.T, baseline='weighted_wiggle')

