
def test_imshow_float128():
    fig, ax = plt.subplots()
    ax.imshow(np.zeros((3, 3), dtype=np.longdouble))
    with (ExitStack() if np.can_cast(np.longdouble, np.float64, "equiv")
          else pytest.warns(UserWarning)):
        # Ensure that drawing doesn't cause crash.
        fig.canvas.draw()

