
def test_multi_font_type3():
    fonts, test_str = _gen_multi_font_text()
    plt.rc('font', family=fonts, size=16)
    plt.rc('pdf', fonttype=3)

    fig = plt.figure(figsize=(8, 6))
    fig.text(0.5, 0.5, test_str,
             horizontalalignment='center', verticalalignment='center')


def test_multi_font_type3():
    fonts, test_str = _gen_multi_font_text()
    plt.rc('font', family=fonts, size=16)
    plt.rc('ps', fonttype=3)

    fig = plt.figure(figsize=(8, 6))
    fig.text(0.5, 0.5, test_str,
             horizontalalignment='center', verticalalignment='center')

