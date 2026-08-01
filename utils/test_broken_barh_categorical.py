
def test_broken_barh_categorical():
    fig, ax = plt.subplots()
    pc = ax.broken_barh([(0, 10)], ('a', 0.8))
    assert tuple(pc.get_datalim(ax.transData).intervaly) == (0, 0.8)

    pc = ax.broken_barh([(0, 10)], ('a', 0.8), align="center")
    assert tuple(pc.get_datalim(ax.transData).intervaly) == (-0.4, 0.4)

    pc = ax.broken_barh([(0, 10)], ('a', 0.8), align="top")
    assert tuple(pc.get_datalim(ax.transData).intervaly) == (-0.8, 0)

