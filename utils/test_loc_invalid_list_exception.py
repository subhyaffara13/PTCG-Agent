
def test_loc_invalid_list_exception():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match=('loc must be string, coordinate '
                       'tuple, or an integer 0-10, not \\[1.1, 2.2, 3.3\\]')):
        ax.legend(loc=[1.1, 2.2, 3.3], labels=["mock data"])

