
def test_log_scales_invalid():
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    with pytest.warns(UserWarning, match='Attempt to set non-positive'):
        ax.set_xlim(-1, 10)
    ax.set_yscale('log')
    with pytest.warns(UserWarning, match='Attempt to set non-positive'):
        ax.set_ylim(-1, 10)

