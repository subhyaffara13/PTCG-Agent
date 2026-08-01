
def test_errorbar_linestyle_type():
    eb = plt.errorbar([1, 2, 3], [1, 2, 3],
                      yerr=[1, 2, 3], elinestyle='--')
    errorlines = eb[-1][0]
    errorlinestyle = errorlines.get_linestyle()
    assert errorlinestyle == [(0, (6, 6))]

