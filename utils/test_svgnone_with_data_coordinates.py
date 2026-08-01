
def test_svgnone_with_data_coordinates():
    plt.rcParams.update({'svg.fonttype': 'none', 'font.stretch': 'condensed'})
    expected = 'Unlikely to appear by chance'

    fig, ax = plt.subplots()
    ax.text(np.datetime64('2019-06-30'), 1, expected)
    ax.set_xlim(np.datetime64('2019-01-01'), np.datetime64('2019-12-31'))
    ax.set_ylim(0, 2)

    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        fd.seek(0)
        buf = fd.read().decode()

    assert expected in buf and "condensed" in buf

