
def test_grouped_bar_hatch_sequence():
    """Each dataset should receive its own hatch pattern when a sequence is passed."""
    fig, ax = plt.subplots()
    x = np.arange(2)
    heights = [np.array([1, 2]), np.array([2, 3]), np.array([3, 4])]
    hatches = ['//', 'xx', '..']
    containers = ax.grouped_bar(heights, positions=x, hatch=hatches)

    # Verify each dataset gets the corresponding hatch
    for hatch, c in zip(hatches, containers.bar_containers):
        for rect in c:
            assert rect.get_hatch() == hatch

