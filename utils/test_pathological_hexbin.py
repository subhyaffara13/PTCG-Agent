
def test_pathological_hexbin():
    # issue #2863
    mylist = [10] * 100
    fig, ax = plt.subplots(1, 1)
    ax.hexbin(mylist, mylist)
    fig.savefig(io.BytesIO())  # Check that no warning is emitted.

