
def test_eventplot_alpha():
    fig, ax = plt.subplots()

    # one alpha for all
    collections = ax.eventplot([[0, 2, 4], [1, 3, 5, 7]], alpha=0.7)
    assert collections[0].get_alpha() == 0.7
    assert collections[1].get_alpha() == 0.7

    # one alpha per collection
    collections = ax.eventplot([[0, 2, 4], [1, 3, 5, 7]], alpha=[0.5, 0.7])
    assert collections[0].get_alpha() == 0.5
    assert collections[1].get_alpha() == 0.7

    with pytest.raises(ValueError, match="alpha and positions are unequal"):
        ax.eventplot([[0, 2, 4], [1, 3, 5, 7]], alpha=[0.5, 0.7, 0.9])

    with pytest.raises(ValueError, match="alpha and positions are unequal"):
        ax.eventplot([0, 2, 4], alpha=[0.5, 0.7])

