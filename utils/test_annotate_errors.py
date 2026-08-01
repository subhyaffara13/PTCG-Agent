
def test_annotate_errors(err, xycoords, match):
    fig, ax = plt.subplots()
    with pytest.raises(err, match=match):
        ax.annotate('xy', (0, 0), xytext=(0.5, 0.5), xycoords=xycoords)
        fig.canvas.draw()

