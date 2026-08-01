
def test_log_transform():
    # Tests that the last line runs without exception (previously the
    # transform would fail if one of the axes was logarithmic).
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    ax.transData.transform((1, 1))

