
def test_contour_shape_error(args, message):
    fig, ax = plt.subplots()
    with pytest.raises(TypeError, match=re.escape(message)):
        ax.contour(*args)

