
def test_close_all_warning():
    fig1 = plt.figure()

    # Check that the warning is issued when 'all' is passed to plt.figure
    with pytest.warns(UserWarning, match="closes all existing figures"):
        fig2 = plt.figure("all")

