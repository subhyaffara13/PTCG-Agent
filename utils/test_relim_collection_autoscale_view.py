
def test_relim_collection_autoscale_view():
    # GH#30859 - end-to-end: after set_offsets(), relim() + autoscale_view()
    # must update the visible axis limits, not just dataLim.
    fig, ax = plt.subplots()
    sc = ax.scatter([], [])
    xs = np.linspace(0, 10, 50)
    sc.set_offsets(np.column_stack((xs, np.sin(xs))))
    ax.relim()
    ax.autoscale_view()
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    # autoscale_view adds a margin, so limits should comfortably contain data
    assert xlim[0] <= 0 and xlim[1] >= 10, f"xlim should contain [0, 10], got {xlim}"
    assert ylim[0] <= -1 and ylim[1] >= 1, f"ylim should contain [-1, 1], got {ylim}"

