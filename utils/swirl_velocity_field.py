
def swirl_velocity_field():
    x = np.linspace(-3., 3., 200)
    y = np.linspace(-3., 3., 100)
    X, Y = np.meshgrid(x, y)
    a = 0.1
    U = np.cos(a) * (-Y) - np.sin(a) * X
    V = np.sin(a) * (-Y) + np.cos(a) * X
    return x, y, U, V

