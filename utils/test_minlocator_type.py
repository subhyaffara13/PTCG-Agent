
def test_minlocator_type():
    fig, ax = plt.subplots()
    with pytest.raises(TypeError):
        ax.xaxis.set_minor_locator(mticker.LogFormatter())

