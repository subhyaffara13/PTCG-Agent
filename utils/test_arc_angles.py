
def test_arc_angles():
    # Ellipse parameters
    w = 2
    h = 1
    centre = (0.2, 0.5)
    scale = 2

    fig, axs = plt.subplots(3, 3)
    for i, ax in enumerate(axs.flat):
        theta2 = i * 360 / 9
        theta1 = theta2 - 45

        ax.add_patch(mpatches.Ellipse(centre, w, h, alpha=0.3))
        ax.add_patch(mpatches.Arc(centre, w, h, theta1=theta1, theta2=theta2))
        # Straight lines intersecting start and end of arc
        ax.plot([scale * np.cos(np.deg2rad(theta1)) + centre[0],
                 centre[0],
                 scale * np.cos(np.deg2rad(theta2)) + centre[0]],
                [scale * np.sin(np.deg2rad(theta1)) + centre[1],
                 centre[1],
                 scale * np.sin(np.deg2rad(theta2)) + centre[1]])

        ax.set_xlim(-scale, scale)
        ax.set_ylim(-scale, scale)

        # This looks the same, but it triggers a different code path when it
        # gets large enough.
        w *= 10
        h *= 10
        centre = (centre[0] * 10, centre[1] * 10)
        scale *= 10

