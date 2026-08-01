
def test_subplot():
    fig = plt.figure(figsize=(5, 5))
    ax = Subplot(fig, 111)
    fig.add_subplot(ax)

