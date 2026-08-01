
def test_corner_mask():
    n = 60
    mask_level = 0.95
    noise_amp = 1.0
    np.random.seed([1])
    x, y = np.meshgrid(np.linspace(0, 2.0, n), np.linspace(0, 2.0, n))
    z = np.cos(7*x)*np.sin(8*y) + noise_amp*np.random.rand(n, n)
    mask = np.random.rand(n, n) >= mask_level
    z = np.ma.array(z, mask=mask)

    for corner_mask in [False, True]:
        plt.figure()
        plt.contourf(z, corner_mask=corner_mask)

