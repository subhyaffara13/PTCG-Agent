
def test_anchored_offsetbox_tuple_and_float_borderpad():
    """
    Test AnchoredOffsetbox correctly handles both float and tuple for borderpad.
    """

    fig, ax = plt.subplots()

    # Case 1: Establish a baseline with float value
    text_float = AnchoredText("float", loc='lower left', borderpad=5)
    ax.add_artist(text_float)

    # Case 2: Test that a symmetric tuple gives the exact same result.
    text_tuple_equal = AnchoredText("tuple", loc='lower left', borderpad=(5, 5))
    ax.add_artist(text_tuple_equal)

    # Case 3: Test that an asymmetric tuple with different values works as expected.
    text_tuple_asym = AnchoredText("tuple_asym", loc='lower left', borderpad=(10, 4))
    ax.add_artist(text_tuple_asym)

    # Draw the canvas to calculate final positions
    fig.canvas.draw()

    pos_float = text_float.get_window_extent()
    pos_tuple_equal = text_tuple_equal.get_window_extent()
    pos_tuple_asym = text_tuple_asym.get_window_extent()

    # Assertion 1: Prove that borderpad=5 is identical to borderpad=(5, 5).
    assert pos_tuple_equal.x0 == pos_float.x0
    assert pos_tuple_equal.y0 == pos_float.y0

    # Assertion 2: Prove that the asymmetric padding moved the box
    # further from the origin than the baseline in the x-direction and less far
    # in the y-direction.
    assert pos_tuple_asym.x0 > pos_float.x0
    assert pos_tuple_asym.y0 < pos_float.y0

