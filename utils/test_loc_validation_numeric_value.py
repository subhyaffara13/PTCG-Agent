
def test_loc_validation_numeric_value():
    fig, ax = plt.subplots()
    ax.legend(loc=0, labels=["mock data"])
    ax.legend(loc=1, labels=["mock data"])
    ax.legend(loc=5, labels=["mock data"])
    ax.legend(loc=10, labels=["mock data"])
    with pytest.raises(ValueError, match=('loc must be string, coordinate '
                       'tuple, or an integer 0-10, not 11')):
        ax.legend(loc=11, labels=["mock data"])

    with pytest.raises(ValueError, match=('loc must be string, coordinate '
                       'tuple, or an integer 0-10, not -1')):
        ax.legend(loc=-1, labels=["mock data"])

