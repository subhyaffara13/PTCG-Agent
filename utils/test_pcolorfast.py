
def test_pcolorfast(xy, data, cls):
    fig, ax = plt.subplots()
    assert type(ax.pcolorfast(*xy, data)) == cls

