
def test_polar_theta_limits():
    r = np.arange(0, 3.0, 0.01)
    theta = 2*np.pi*r

    theta_mins = np.arange(15.0, 361.0, 90.0)
    theta_maxs = np.arange(50.0, 361.0, 90.0)
    DIRECTIONS = ('out', 'in', 'inout')

    fig, axs = plt.subplots(len(theta_mins), len(theta_maxs),
                            subplot_kw={'polar': True},
                            figsize=(8, 6))

    for i, start in enumerate(theta_mins):
        for j, end in enumerate(theta_maxs):
            ax = axs[i, j]
            ax.plot(theta, r)
            if start < end:
                ax.set_thetamin(start)
                ax.set_thetamax(end)
            else:
                # Plot with clockwise orientation instead.
                ax.set_thetamin(end)
                ax.set_thetamax(start)
                ax.set_theta_direction('clockwise')
            ax.tick_params(tick1On=True, tick2On=True,
                           direction=DIRECTIONS[i % len(DIRECTIONS)],
                           rotation='auto')
            ax.yaxis.set_tick_params(label2On=True, rotation='auto')
            ax.xaxis.get_major_locator().base.set_params(  # backcompat
                steps=[1, 2, 2.5, 5, 10])

