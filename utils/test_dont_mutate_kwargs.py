
def test_dont_mutate_kwargs():
    subplot_kw = {'sharex': 'all'}
    gridspec_kw = {'width_ratios': [1, 2]}
    fig, ax = plt.subplots(1, 2, subplot_kw=subplot_kw,
                           gridspec_kw=gridspec_kw)
    assert subplot_kw == {'sharex': 'all'}
    assert gridspec_kw == {'width_ratios': [1, 2]}

