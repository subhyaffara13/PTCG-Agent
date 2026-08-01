
def test_transparent_markers():
    np.random.seed(0)
    data = np.random.random(50)

    fig, ax = plt.subplots()
    ax.plot(data, 'D', mfc='none', markersize=100)

