
def test_rotate():
    A = [0, 1, 2, 3, 4]

    assert rotate_left(A, 2) == [2, 3, 4, 0, 1]
    assert rotate_right(A, 1) == [4, 0, 1, 2, 3]
    A = []
    B = rotate_right(A, 1)
    assert B == []
    B.append(1)
    assert A == []
    B = rotate_left(A, 1)
    assert B == []
    B.append(1)
    assert A == []


def test_rotate(style):
    """Test rotating using the left mouse button."""
    if style == 'azel':
        s = 0.5
    else:
        s = mpl.rcParams['axes3d.trackballsize'] / 2
    s *= 0.5
    mpl.rcParams['axes3d.trackballborder'] = 0
    with mpl.rc_context({'axes3d.mouserotationstyle': style}):
        for roll, dx, dy in [
                [0, 1, 0],
                [30, 1, 0],
                [0, 0, 1],
                [30, 0, 1],
                [0, 0.5, np.sqrt(3)/2],
                [30, 0.5, np.sqrt(3)/2],
                [0, 2, 0]]:
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, projection='3d')
            ax.view_init(0, 0, roll)
            ax.figure.canvas.draw()

            # drag mouse to change orientation
            MouseEvent._from_ax_coords(
                "button_press_event", ax, (0, 0), MouseButton.LEFT)._process()
            MouseEvent._from_ax_coords(
                "motion_notify_event", ax, (s*dx*ax._pseudo_w, s*dy*ax._pseudo_h),
                MouseButton.LEFT)._process()
            ax.figure.canvas.draw()

            c = np.sqrt(3)/2
            expectations = {
                ('azel', 0, 1, 0): (0, -45, 0),
                ('azel', 0, 0, 1): (-45, 0, 0),
                ('azel', 0, 0.5, c): (-38.971143, -22.5, 0),
                ('azel', 0, 2, 0): (0, -90, 0),
                ('azel', 30, 1, 0): (22.5, -38.971143, 30),
                ('azel', 30, 0, 1): (-38.971143, -22.5, 30),
                ('azel', 30, 0.5, c): (-22.5, -38.971143, 30),

                ('trackball', 0, 1, 0): (0, -28.64789, 0),
                ('trackball', 0, 0, 1): (-28.64789, 0, 0),
                ('trackball', 0, 0.5, c): (-24.531578, -15.277726, 3.340403),
                ('trackball', 0, 2, 0): (0, -180/np.pi, 0),
                ('trackball', 30, 1, 0): (13.869588, -25.319385, 26.87008),
                ('trackball', 30, 0, 1): (-24.531578, -15.277726, 33.340403),
                ('trackball', 30, 0.5, c): (-13.869588, -25.319385, 33.129920),

                ('sphere', 0, 1, 0): (0, -30, 0),
                ('sphere', 0, 0, 1): (-30, 0, 0),
                ('sphere', 0, 0.5, c): (-25.658906, -16.102114, 3.690068),
                ('sphere', 0, 2, 0): (0, -90, 0),
                ('sphere', 30, 1, 0): (14.477512, -26.565051, 26.565051),
                ('sphere', 30, 0, 1): (-25.658906, -16.102114, 33.690068),
                ('sphere', 30, 0.5, c): (-14.477512, -26.565051, 33.434949),

                ('arcball', 0, 1, 0): (0, -60, 0),
                ('arcball', 0, 0, 1): (-60, 0, 0),
                ('arcball', 0, 0.5, c): (-48.590378, -40.893395, 19.106605),
                ('arcball', 0, 2, 0): (0, 180, 0),
                ('arcball', 30, 1, 0): (25.658906, -56.309932, 16.102114),
                ('arcball', 30, 0, 1): (-48.590378, -40.893395, 49.106605),
                ('arcball', 30, 0.5, c): (-25.658906, -56.309932, 43.897886)}
            new_elev, new_azim, new_roll = expectations[(style, roll, dx, dy)]
            np.testing.assert_allclose((ax.elev, ax.azim, ax.roll),
                                       (new_elev, new_azim, new_roll), atol=1e-6)

