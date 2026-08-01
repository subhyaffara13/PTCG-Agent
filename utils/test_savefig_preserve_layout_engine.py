
def test_savefig_preserve_layout_engine():
    fig = plt.figure(layout='compressed')
    fig.savefig(io.BytesIO(), bbox_inches='tight')

    assert fig.get_layout_engine()._compress

