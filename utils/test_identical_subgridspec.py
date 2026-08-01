
def test_identical_subgridspec():

    fig = plt.figure(constrained_layout=True)

    GS = fig.add_gridspec(2, 1)

    GSA = GS[0].subgridspec(1, 3)
    GSB = GS[1].subgridspec(1, 3)

    axa = []
    axb = []
    for i in range(3):
        axa += [fig.add_subplot(GSA[i])]
        axb += [fig.add_subplot(GSB[i])]

    fig.draw_without_rendering()
    # check first row above second
    assert axa[0].get_position().y0 > axb[0].get_position().y1

