
def test_int_fmt_bar_label():
    fig, ax = plt.subplots()
    bars = ax.bar(['foo', 'bar'], [5, 7])
    labels = ax.bar_label(bars, fmt='{:d}')
    assert [l.get_text() for l in labels] == ['5', '7']

