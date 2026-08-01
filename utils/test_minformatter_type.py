
def test_minformatter_type():
    fig, ax = plt.subplots()
    with pytest.raises(TypeError):
        ax.xaxis.set_minor_formatter(mticker.LogLocator())

