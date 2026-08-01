
def test_empty_fancyarrow():
    fig, ax = plt.subplots()
    arrow = ax.arrow([], [], [], [])
    assert arrow is not None

