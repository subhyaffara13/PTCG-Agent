
def test_connection_patch():
    fig, (ax1, ax2) = plt.subplots(1, 2)

    con = mpatches.ConnectionPatch(xyA=(0.1, 0.1), xyB=(0.9, 0.9),
                                   coordsA='data', coordsB='data',
                                   axesA=ax2, axesB=ax1,
                                   arrowstyle="->")
    ax2.add_artist(con)

    xyA = (0.6, 1.0)  # in axes coordinates
    xyB = (0.0, 0.2)  # x in axes coordinates, y in data coordinates
    coordsA = "axes fraction"
    coordsB = ax2.get_yaxis_transform()
    con = mpatches.ConnectionPatch(xyA=xyA, xyB=xyB, coordsA=coordsA,
                                   coordsB=coordsB, arrowstyle="-")
    ax2.add_artist(con)

