
def test_url_tick(monkeypatch):
    monkeypatch.setenv('SOURCE_DATE_EPOCH', '19680801')

    fig1, ax = plt.subplots()
    ax.scatter([1, 2, 3], [4, 5, 6])
    for i, tick in enumerate(ax.yaxis.get_major_ticks()):
        tick.set_url(f'https://example.com/{i}')

    fig2, ax = plt.subplots()
    ax.scatter([1, 2, 3], [4, 5, 6])
    for i, tick in enumerate(ax.yaxis.get_major_ticks()):
        tick.label1.set_url(f'https://example.com/{i}')
        tick.label2.set_url(f'https://example.com/{i}')

    b1 = BytesIO()
    fig1.savefig(b1, format='svg')
    b1 = b1.getvalue()

    b2 = BytesIO()
    fig2.savefig(b2, format='svg')
    b2 = b2.getvalue()

    for i in range(len(ax.yaxis.get_major_ticks())):
        assert f'https://example.com/{i}'.encode('ascii') in b1
    assert b1 == b2

