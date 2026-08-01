
def test_manage_xticks():
    _, ax = plt.subplots()
    ax.set_xlim(0, 4)
    old_xlim = ax.get_xlim()
    np.random.seed(0)
    y1 = np.random.normal(10, 3, 20)
    y2 = np.random.normal(3, 1, 20)
    ax.boxplot([y1, y2], positions=[1, 2], manage_ticks=False)
    new_xlim = ax.get_xlim()
    assert_array_equal(old_xlim, new_xlim)

