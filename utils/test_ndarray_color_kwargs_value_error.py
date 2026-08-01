
def test_ndarray_color_kwargs_value_error():
    # smoke test
    # ensures ndarray can be passed to color in kwargs for 3d projection plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(1, 0, 0, color=np.array([0, 0, 0, 1]))
    fig.canvas.draw()

