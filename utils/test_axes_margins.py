
def test_axes_margins():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2, 3])
    assert ax.get_ybound()[0] != 0

    fig, ax = plt.subplots()
    ax.bar([0, 1, 2, 3], [1, 1, 1, 1])
    assert ax.get_ybound()[0] == 0

    fig, ax = plt.subplots()
    ax.barh([0, 1, 2, 3], [1, 1, 1, 1])
    assert ax.get_xbound()[0] == 0

    fig, ax = plt.subplots()
    ax.pcolor(np.zeros((10, 10)))
    assert ax.get_xbound() == (0, 10)
    assert ax.get_ybound() == (0, 10)

    fig, ax = plt.subplots()
    ax.pcolorfast(np.zeros((10, 10)))
    assert ax.get_xbound() == (0, 10)
    assert ax.get_ybound() == (0, 10)

    fig, ax = plt.subplots()
    ax.hist(np.arange(10))
    assert ax.get_ybound()[0] == 0

    fig, ax = plt.subplots()
    ax.imshow(np.zeros((10, 10)))
    assert ax.get_xbound() == (-0.5, 9.5)
    assert ax.get_ybound() == (-0.5, 9.5)

