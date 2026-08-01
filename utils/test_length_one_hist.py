
def test_length_one_hist():
    fig, ax = plt.subplots()
    ax.hist(1)
    ax.hist([1])

