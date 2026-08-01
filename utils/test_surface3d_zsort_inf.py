
def test_surface3d_zsort_inf():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x, y = np.mgrid[-2:2:0.1, -2:2:0.1]
    z = np.sin(x)**2 + np.cos(y)**2
    z[x.shape[0] // 2:, x.shape[1] // 2:] = np.inf

    ax.plot_surface(x, y, z, cmap='jet')
    ax.view_init(elev=45, azim=145)

