
def test_imshow_float16():
    fig, ax = plt.subplots()
    ax.imshow(np.zeros((3, 3), dtype=np.float16))
    # Ensure that drawing doesn't cause crash.
    fig.canvas.draw()

