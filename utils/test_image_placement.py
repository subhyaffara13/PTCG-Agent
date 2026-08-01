
def test_image_placement():
    """
    The red box should line up exactly with the outside of the image.
    """
    fig, ax = plt.subplots()
    ax.plot([0, 0, 1, 1, 0], [0, 1, 1, 0, 0], color='r', lw=0.1)
    np.random.seed(19680801)
    ax.imshow(np.random.randn(16, 16), cmap='Blues', extent=(0, 1, 0, 1),
              interpolation='none', vmin=-1, vmax=1)
    ax.set_xlim(-0.1, 1+0.1)
    ax.set_ylim(-0.1, 1+0.1)

