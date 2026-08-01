
def test_layout_leak():
    # Make sure there aren't any cyclic references when using LayoutGrid
    # GH #25853
    fig = plt.figure(constrained_layout=True, figsize=(10, 10))
    fig.add_subplot()
    fig.draw_without_rendering()
    plt.close("all")
    del fig
    gc.collect()
    assert not any(isinstance(obj, mpl._layoutgrid.LayoutGrid)
                   for obj in gc.get_objects())

