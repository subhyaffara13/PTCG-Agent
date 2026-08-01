
def test_hexbin_pickable():
    # From #1973: Test that picking a hexbin collection works
    fig, ax = plt.subplots()
    data = (np.arange(200) / 200).reshape((2, 100))
    x, y = data
    hb = ax.hexbin(x, y, extent=[.1, .3, .6, .7], picker=-1)
    mouse_event = SimpleNamespace(x=400, y=300)
    assert hb.contains(mouse_event)[0]

