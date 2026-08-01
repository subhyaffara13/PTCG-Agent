
def test_loc_valid_tuple():
    fig, ax = plt.subplots()
    ax.legend(loc=(0.481, 0.442), labels=["mock data"])
    ax.legend(loc=(1, 2), labels=["mock data"])

