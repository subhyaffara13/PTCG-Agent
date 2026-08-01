
def test_contour3d_extend3d():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.contour(X, Y, Z, zdir='z', offset=-100, cmap="coolwarm", extend3d=True)
    ax.set_xlim(-30, 30)
    ax.set_ylim(-20, 40)
    ax.set_zlim(-80, 80)

