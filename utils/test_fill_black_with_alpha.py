
def test_fill_black_with_alpha():
    fig, ax = plt.subplots()
    ax.scatter(x=[0, 0.1, 1], y=[0, 0, 0], c='k', alpha=0.1, s=10000)

