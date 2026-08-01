
def test_patchcollection_legend_empty():
    # Test that empty PatchCollection doesn't crash
    fig, ax = plt.subplots()

    # Create an empty PatchCollection
    pc = mcollections.PatchCollection([], label="empty collection")
    ax.add_collection(pc)

    # This should not crash
    leg = ax.legend()

    # Check that the label still appears
    assert len(leg.get_texts()) == 1
    assert leg.get_texts()[0].get_text() == "empty collection"

    # The legend handle should exist
    assert len(leg.legend_handles) == 1

