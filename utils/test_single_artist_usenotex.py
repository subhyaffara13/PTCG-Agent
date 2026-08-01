
def test_single_artist_usenotex(fmt):
    # Check that a single artist can be marked as not-usetex even though the
    # rcParam is on ("2_2_2" fails if passed to TeX).  This currently skips
    # postscript output as the ps renderer doesn't support mixing usetex and
    # non-usetex.
    plt.rcParams["text.usetex"] = True
    fig = plt.figure()
    fig.text(.5, .5, "2_2_2", usetex=False)
    fig.savefig(io.BytesIO(), format=fmt)

