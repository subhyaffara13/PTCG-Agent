
def test_imshow_quantitynd():
    # generate a dummy ndarray subclass
    arr = QuantityND(np.ones((2, 2)), "m")
    fig, ax = plt.subplots()
    ax.imshow(arr)
    # executing the draw should not raise an exception
    fig.canvas.draw()

