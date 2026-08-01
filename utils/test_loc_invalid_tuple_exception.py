
def test_loc_invalid_tuple_exception():
    # check that exception is raised if the loc arg
    # of legend is not a 2-tuple of numbers
    fig, ax = plt.subplots()
    with pytest.raises(ValueError, match=('loc must be string, coordinate '
                       'tuple, or an integer 0-10, not \\(1.1,\\)')):
        ax.legend(loc=(1.1, ), labels=["mock data"])

    with pytest.raises(ValueError, match=('loc must be string, coordinate '
                       'tuple, or an integer 0-10, not \\(0.481, 0.4227, 0.4523\\)')):
        ax.legend(loc=(0.481, 0.4227, 0.4523), labels=["mock data"])

    with pytest.raises(ValueError, match=('loc must be string, coordinate '
                       'tuple, or an integer 0-10, not \\(0.481, \'go blue\'\\)')):
        ax.legend(loc=(0.481, "go blue"), labels=["mock data"])

