
def test_contourf3d():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)
    ax.contourf(X, Y, Z, zdir='z', offset=-100, cmap="coolwarm")
    ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap="coolwarm")
    ax.contourf(X, Y, Z, zdir='y', offset=40, cmap="coolwarm")
    ax.set_xlim(-40, 40)
    ax.set_ylim(-40, 40)
    ax.set_zlim(-100, 100)

