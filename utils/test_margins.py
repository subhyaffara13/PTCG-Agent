
def test_margins():
    a = np.array([1])
    m = margins(a)
    assert_equal(len(m), 1)
    m0 = m[0]
    assert_array_equal(m0, np.array([1]))

    a = np.array([[1]])
    m0, m1 = margins(a)
    expected0 = np.array([[1]])
    expected1 = np.array([[1]])
    assert_array_equal(m0, expected0)
    assert_array_equal(m1, expected1)

    a = np.arange(12).reshape(2, 6)
    m0, m1 = margins(a)
    expected0 = np.array([[15], [51]])
    expected1 = np.array([[6, 8, 10, 12, 14, 16]])
    assert_array_equal(m0, expected0)
    assert_array_equal(m1, expected1)

    a = np.arange(24).reshape(2, 3, 4)
    m0, m1, m2 = margins(a)
    expected0 = np.array([[[66]], [[210]]])
    expected1 = np.array([[[60], [92], [124]]])
    expected2 = np.array([[[60, 66, 72, 78]]])
    assert_array_equal(m0, expected0)
    assert_array_equal(m1, expected1)
    assert_array_equal(m2, expected2)


def test_margins():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.margins(0.2)
    assert ax.margins() == (0.2, 0.2, 0.2)
    ax.margins(0.1, 0.2, 0.3)
    assert ax.margins() == (0.1, 0.2, 0.3)
    ax.margins(x=0)
    assert ax.margins() == (0, 0.2, 0.3)
    ax.margins(y=0.1)
    assert ax.margins() == (0, 0.1, 0.3)
    ax.margins(z=0)
    assert ax.margins() == (0, 0.1, 0)


def test_margins():
    # test all ways margins can be called
    data = [1, 10]
    xmin = 0.0
    xmax = len(data) - 1.0
    ymin = min(data)
    ymax = max(data)

    fig1, ax1 = plt.subplots(1, 1)
    ax1.plot(data)
    ax1.margins(1)
    assert ax1.margins() == (1, 1)
    assert ax1.get_xlim() == (xmin - (xmax - xmin) * 1,
                              xmax + (xmax - xmin) * 1)
    assert ax1.get_ylim() == (ymin - (ymax - ymin) * 1,
                              ymax + (ymax - ymin) * 1)

    fig2, ax2 = plt.subplots(1, 1)
    ax2.plot(data)
    ax2.margins(0.5, 2)
    assert ax2.margins() == (0.5, 2)
    assert ax2.get_xlim() == (xmin - (xmax - xmin) * 0.5,
                              xmax + (xmax - xmin) * 0.5)
    assert ax2.get_ylim() == (ymin - (ymax - ymin) * 2,
                              ymax + (ymax - ymin) * 2)

    fig3, ax3 = plt.subplots(1, 1)
    ax3.plot(data)
    ax3.margins(x=-0.2, y=0.5)
    assert ax3.margins() == (-0.2, 0.5)
    assert ax3.get_xlim() == (xmin - (xmax - xmin) * -0.2,
                              xmax + (xmax - xmin) * -0.2)
    assert ax3.get_ylim() == (ymin - (ymax - ymin) * 0.5,
                              ymax + (ymax - ymin) * 0.5)

