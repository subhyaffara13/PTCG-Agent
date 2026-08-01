
def test_hist_density():
    np.random.seed(19680801)
    data = np.random.standard_normal(2000)
    fig, ax = plt.subplots()
    ax.hist(data, density=True)

