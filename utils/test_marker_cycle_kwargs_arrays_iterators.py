
def test_marker_cycle_kwargs_arrays_iterators():
    fig, ax = plt.subplots()
    ax.set_prop_cycle(c=np.array(['r', 'g', 'y']),
                      marker=iter(['.', '*', 'x']))
    for _ in range(4):
        ax.plot(range(10), range(10))
    assert [l.get_color() for l in ax.lines] == ['r', 'g', 'y', 'r']
    assert [l.get_marker() for l in ax.lines] == ['.', '*', 'x', '.']

