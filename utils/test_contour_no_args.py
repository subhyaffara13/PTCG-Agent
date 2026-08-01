
def test_contour_no_args():
    fig, ax = plt.subplots()
    data = [[0, 1], [1, 0]]
    with pytest.raises(TypeError, match=r"contour\(\) takes from 1 to 4"):
        ax.contour(Z=data)

