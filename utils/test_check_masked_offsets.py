
def test_check_masked_offsets():
    # Check if masked data is respected by scatter
    # Ref: Issue #24545
    unmasked_x = [
        datetime(2022, 12, 15, 4, 49, 52),
        datetime(2022, 12, 15, 4, 49, 53),
        datetime(2022, 12, 15, 4, 49, 54),
        datetime(2022, 12, 15, 4, 49, 55),
        datetime(2022, 12, 15, 4, 49, 56),
    ]

    masked_y = np.ma.array([1, 2, 3, 4, 5], mask=[0, 1, 1, 0, 0])

    fig, ax = plt.subplots()
    ax.scatter(unmasked_x, masked_y)

