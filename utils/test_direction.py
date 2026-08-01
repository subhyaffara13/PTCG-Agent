
def test_direction():
    x, y, U, V = swirl_velocity_field()
    plt.streamplot(x, y, U, V, integration_direction='backward',
                   maxlength=1.5, start_points=[[1.5, 0.]],
                   linewidth=2, density=2)

