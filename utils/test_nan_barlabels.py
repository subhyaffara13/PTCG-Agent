
def test_nan_barlabels():
    fig, ax = plt.subplots()
    bars = ax.bar([1, 2, 3], [np.nan, 1, 2], yerr=[0.2, 0.4, 0.6])
    labels = ax.bar_label(bars)
    assert [l.get_text() for l in labels] == ['', '1', '2']
    assert np.allclose(ax.get_ylim(), (0.0, 3.0))

    fig, ax = plt.subplots()
    bars = ax.bar([1, 2, 3], [0, 1, 2], yerr=[0.2, np.nan, 0.6])
    labels = ax.bar_label(bars)
    assert [l.get_text() for l in labels] == ['0', '1', '2']
    assert np.allclose(ax.get_ylim(), (-0.5, 3.0))

    fig, ax = plt.subplots()
    bars = ax.bar([1, 2, 3], [np.nan, 1, 2], yerr=[np.nan, np.nan, 0.6])
    labels = ax.bar_label(bars)
    assert [l.get_text() for l in labels] == ['', '1', '2']
    assert np.allclose(ax.get_ylim(), (0.0, 3.0))

