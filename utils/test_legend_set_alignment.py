
def test_legend_set_alignment(alignment):
    fig, ax = plt.subplots()
    ax.plot(range(10), label='test')
    leg = ax.legend()
    leg.set_alignment(alignment)
    assert leg.get_children()[0].align == alignment
    assert leg.get_alignment() == alignment

