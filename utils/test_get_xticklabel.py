
def test_get_xticklabel():
    fig, ax = plt.subplots()
    ax.plot(np.arange(10))
    for ind in range(10):
        assert ax.get_xticklabels()[ind].get_text() == f'{ind}'
        assert ax.get_yticklabels()[ind].get_text() == f'{ind}'

