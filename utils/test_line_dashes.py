
def test_line_dashes():
    # Tolerance introduced after reordering of floating-point operations
    # Remove when regenerating the images
    fig, ax = plt.subplots()

    ax.plot(range(10), linestyle=(0, (3, 3)), lw=5)

