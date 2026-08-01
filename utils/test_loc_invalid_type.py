
def test_loc_invalid_type():
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match=("loc must be string, coordinate "
                       "tuple, or an integer 0-10, not {'not': True}")):
        ax.legend(loc={'not': True}, labels=["mock data"])

