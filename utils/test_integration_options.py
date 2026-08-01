
def test_integration_options():
    # Linear potential flow over a lifting cylinder
    n = 50
    x, y = np.meshgrid(np.linspace(-2, 2, n), np.linspace(-3, 3, n))
    th = np.arctan2(y, x)
    r = np.sqrt(x**2 + y**2)
    vr = -np.cos(th) / r**2
    vt = -np.sin(th) / r**2 - 1 / r
    vx = vr * np.cos(th) - vt * np.sin(th) + 1.0
    vy = vr * np.sin(th) + vt * np.cos(th)

    # Seed points
    n_seed = 50
    seed_pts = np.column_stack((np.full(n_seed, -1.75), np.linspace(-2, 2, n_seed)))

    fig, axs = plt.subplots(3, 1, figsize=(6, 14))
    th_circ = np.linspace(0, 2 * np.pi, 100)
    for ax, max_val in zip(axs, [0.05, 1, 5]):
        ax_ins = ax.inset_axes([0.0, 0.7, 0.3, 0.35])
        for ax_curr, is_inset in zip([ax, ax_ins], [False, True]):
            ax_curr.streamplot(
                x,
                y,
                vx,
                vy,
                start_points=seed_pts,
                broken_streamlines=False,
                arrowsize=1e-10,
                linewidth=2 if is_inset else 0.6,
                color="k",
                integration_max_step_scale=max_val,
                integration_max_error_scale=max_val,
            )

            # Draw the cylinder
            ax_curr.fill(
                np.cos(th_circ),
                np.sin(th_circ),
                color="w",
                ec="k",
                lw=6 if is_inset else 2,
            )

            # Set axis properties
            ax_curr.set_aspect("equal")

        # Set axis limits and show zoomed region
        ax_ins.set_xlim(-1.2, -0.7)
        ax_ins.set_ylim(-0.8, -0.4)
        ax_ins.set_yticks(())
        ax_ins.set_xticks(())

        ax.set_ylim(-1.5, 1.5)
        ax.axis("off")
        ax.indicate_inset_zoom(ax_ins, ec="k")

    fig.tight_layout()

