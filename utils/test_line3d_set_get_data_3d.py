
def test_line3d_set_get_data_3d():
    x, y, z = [0, 1], [2, 3], [4, 5]
    x2, y2, z2 = [6, 7], [8, 9], [10, 11]
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    lines = ax.plot(x, y, z)
    line = lines[0]
    np.testing.assert_array_equal((x, y, z), line.get_data_3d())
    line.set_data_3d(x2, y2, z2)
    np.testing.assert_array_equal((x2, y2, z2), line.get_data_3d())
    line.set_xdata(x)
    line.set_ydata(y)
    line.set_3d_properties(zs=z, zdir='z')
    np.testing.assert_array_equal((x, y, z), line.get_data_3d())
    line.set_3d_properties(zs=0, zdir='z')
    np.testing.assert_array_equal((x, y, np.zeros_like(z)), line.get_data_3d())

