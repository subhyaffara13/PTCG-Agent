
def test_subfigure_simple():
    # smoketest that subfigures can work...
    fig = plt.figure()
    sf = fig.subfigures(1, 2)
    ax = sf[0].add_subplot(1, 1, 1, projection='3d')
    ax = sf[1].add_subplot(1, 1, 1, projection='3d', label='other')

