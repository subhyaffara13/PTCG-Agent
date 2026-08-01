
def test_majlocator_type():
    fig, ax = plt.subplots()
    with pytest.raises(TypeError):
        ax.xaxis.set_major_locator(mticker.LogFormatter())

