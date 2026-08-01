
def test_majformatter_type():
    fig, ax = plt.subplots()
    with pytest.raises(TypeError):
        ax.xaxis.set_major_formatter(mticker.LogLocator())

