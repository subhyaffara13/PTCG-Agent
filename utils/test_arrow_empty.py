
def test_arrow_empty():
    _, ax = plt.subplots()
    # Create an empty FancyArrow
    ax.arrow(0, 0, 0, 0, head_length=0)

