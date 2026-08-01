
def test_check_offsets_dtype():
    # Check that setting offsets doesn't change dtype
    x = np.ma.array([1, 2, 3, 4, 5], mask=[0, 0, 1, 1, 0])
    y = np.arange(1, 6)

    fig, ax = plt.subplots()
    scat = ax.scatter(x, y)
    masked_offsets = np.ma.column_stack([x, y])
    scat.set_offsets(masked_offsets)
    assert isinstance(scat.get_offsets(), type(masked_offsets))

    unmasked_offsets = np.column_stack([x, y])
    scat.set_offsets(unmasked_offsets)
    assert isinstance(scat.get_offsets(), type(unmasked_offsets))

