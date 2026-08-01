
def test_distributions_submodule():
    actual = set(scipy.stats.distributions.__all__)
    continuous = [dist[0] for dist in distcont]    # continuous dist names
    discrete = [dist[0] for dist in distdiscrete]  # discrete dist names
    other = ['rv_discrete', 'rv_continuous', 'rv_histogram',
             'entropy']
    expected = continuous + discrete + other

    # need to remove, e.g.,
    # <scipy.stats._continuous_distns.trapezoid_gen at 0x1df83bbc688>
    expected = set(filter(lambda s: not str(s).startswith('<'), expected))

    assert actual == expected

