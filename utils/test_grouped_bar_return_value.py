
def test_grouped_bar_return_value():
    fig, ax = plt.subplots()
    ret = ax.grouped_bar([[1, 2, 3], [11, 12, 13]], tick_labels=['A', 'B', 'C'])

    assert len(ret.bar_containers) == 2
    for bc in ret.bar_containers:
        assert isinstance(bc, BarContainer)
        assert bc in ax.containers

    ret.remove()
    for bc in ret.bar_containers:
        assert bc not in ax.containers

