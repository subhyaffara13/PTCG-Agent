
def test_hist_log():
    data0 = np.linspace(0, 1, 200)**3
    data = np.concatenate([1 - data0, 1 + data0])
    fig, ax = plt.subplots()
    ax.hist(data, fill=False, log=True)

