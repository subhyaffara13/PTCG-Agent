
def test_contour_singular_color():
    with pytest.raises(TypeError):
        plt.figure().add_subplot().contour([[0, 1], [2, 3]], color="r")

