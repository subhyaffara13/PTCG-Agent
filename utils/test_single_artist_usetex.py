
def test_single_artist_usetex():
    # Check that a single artist marked with usetex does not get passed through
    # the mathtext parser at all (for the Agg backend) (the mathtext parser
    # currently fails to parse \frac12, requiring \frac{1}{2} instead).
    fig = plt.figure()
    fig.text(.5, .5, r"$\frac12$", usetex=True)
    fig.canvas.draw()

