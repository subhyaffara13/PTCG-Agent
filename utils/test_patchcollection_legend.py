
def test_patchcollection_legend():
    # Test that PatchCollection labels show up in legend and preserve visual
    # properties (issue #23998)
    fig, ax = plt.subplots()

    pc = mcollections.PatchCollection(
        [mpatches.Circle((0, 0), 1), mpatches.Circle((2, 0), 1)],
        label="patch collection",
        facecolor='red',
        edgecolor='blue',
        linewidths=3,
        linestyle='--',
    )
    ax.add_collection(pc)
    ax.autoscale_view()

    leg = ax.legend()

    # Check that the legend contains our label
    assert len(leg.get_texts()) == 1
    assert leg.get_texts()[0].get_text() == "patch collection"

    # Check that the legend handle exists and has correct visual properties
    assert len(leg.legend_handles) == 1
    legend_patch = leg.legend_handles[0]
    assert mpl.colors.same_color(legend_patch.get_facecolor(),
                                  pc.get_facecolor()[0])
    assert mpl.colors.same_color(legend_patch.get_edgecolor(),
                                  pc.get_edgecolor()[0])
    assert legend_patch.get_linewidth() == pc.get_linewidths()[0]
    assert legend_patch.get_linestyle() == pc.get_linestyles()[0]

