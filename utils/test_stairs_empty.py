
def test_stairs_empty():
    ax = plt.figure().add_subplot()
    ax.stairs([], [42])
    assert ax.get_xlim() == (39, 45)
    assert ax.get_ylim() == (-0.06, 0.06)

