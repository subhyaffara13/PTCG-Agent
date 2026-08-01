
def test_secondary_init_xticks():
    fig, ax = plt.subplots()
    secax = ax.secondary_xaxis(1, xticks=[0, 1])
    assert isinstance(secax.xaxis.get_major_locator(), mticker.FixedLocator)
    with pytest.raises(TypeError):
        secax.set_yticks([0, 1])
    secax = ax.secondary_yaxis(1, yticks=[0, 1])
    assert isinstance(secax.yaxis.get_major_locator(), mticker.FixedLocator)
    with pytest.raises(TypeError):
        secax.set_xticks([0, 1])

