
def test_empty_ticks_fixed_loc():
    # Smoke test that [] can be used to unset all tick labels
    fig, ax = plt.subplots()
    ax.bar([1, 2], [1, 2])
    ax.set_xticks([1, 2])
    ax.set_xticklabels([])

