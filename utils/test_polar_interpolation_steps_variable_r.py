
def test_polar_interpolation_steps_variable_r(fig_test, fig_ref):
    l, = fig_test.add_subplot(projection="polar").plot([0, np.pi/2], [1, 2])
    l.get_path()._interpolation_steps = 100
    fig_ref.add_subplot(projection="polar").plot(
        np.linspace(0, np.pi/2, 101), np.linspace(1, 2, 101))


def test_polar_interpolation_steps_variable_r(fig_test, fig_ref):
    l, = fig_test.add_subplot(projection="polar").plot([0, np.pi/2], [1, 2])
    l.get_path()._interpolation_steps = 100
    fig_ref.add_subplot(projection="polar").plot(
        np.linspace(0, np.pi/2, 101), np.linspace(1, 2, 101))

