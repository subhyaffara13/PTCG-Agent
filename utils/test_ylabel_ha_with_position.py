
def test_ylabel_ha_with_position(ha):
    fig = Figure()
    ax = fig.subplots()
    ax.set_ylabel("test", y=1, ha=ha)
    ax.yaxis.set_label_position("right")
    assert ax.yaxis.label.get_ha() == ha

