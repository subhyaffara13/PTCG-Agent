
def test_get_window_extent_wrapped():
    # Test that a long title that wraps to two lines has the same vertical
    # extent as an explicit two line title.

    fig1 = plt.figure(figsize=(3, 3))
    fig1.suptitle("suptitle that is clearly too long in this case", wrap=True)
    window_extent_test = fig1._suptitle.get_window_extent()

    fig2 = plt.figure(figsize=(3, 3))
    fig2.suptitle("suptitle that is clearly\ntoo long in this case")
    window_extent_ref = fig2._suptitle.get_window_extent()

    assert window_extent_test.y0 == window_extent_ref.y0
    assert window_extent_test.y1 == window_extent_ref.y1

