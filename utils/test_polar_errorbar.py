
def test_polar_errorbar(order):
    theta = np.arange(0, 2 * np.pi, np.pi / 8)
    r = theta / np.pi / 2 + 0.5
    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(projection='polar')
    if order == "before":
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.errorbar(theta, r, xerr=0.1, yerr=0.1, capsize=7, fmt="o", c="seagreen")
    else:
        ax.errorbar(theta, r, xerr=0.1, yerr=0.1, capsize=7, fmt="o", c="seagreen")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)

