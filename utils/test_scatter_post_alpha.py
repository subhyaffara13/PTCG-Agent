
def test_scatter_post_alpha():
    fig, ax = plt.subplots()
    sc = ax.scatter(range(5), range(5), c=range(5))
    sc.set_alpha(.1)

