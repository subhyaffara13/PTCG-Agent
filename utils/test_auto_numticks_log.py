
def test_auto_numticks_log():
    # Verify that there are not too many ticks with a large log range.
    fig, ax = plt.subplots()
    mpl.rcParams['axes.autolimit_mode'] = 'round_numbers'
    ax.loglog([1e-20, 1e5], [1e-16, 10])
    assert_array_equal(np.log10(ax.get_xticks()), np.arange(-26, 11, 4))
    assert_array_equal(np.log10(ax.get_yticks()), np.arange(-20, 5, 3))

