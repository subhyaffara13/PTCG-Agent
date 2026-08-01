
def test_invalid_log_lims():
    # Check that invalid log scale limits are ignored
    fig, ax = plt.subplots()
    ax.scatter(range(0, 4), range(0, 4))

    ax.set_xscale('log')
    original_xlim = ax.get_xlim()
    with pytest.warns(UserWarning):
        ax.set_xlim(left=0)
    assert ax.get_xlim() == original_xlim
    with pytest.warns(UserWarning):
        ax.set_xlim(right=-1)
    assert ax.get_xlim() == original_xlim

    ax.set_yscale('log')
    original_ylim = ax.get_ylim()
    with pytest.warns(UserWarning):
        ax.set_ylim(bottom=0)
    assert ax.get_ylim() == original_ylim
    with pytest.warns(UserWarning):
        ax.set_ylim(top=-1)
    assert ax.get_ylim() == original_ylim

