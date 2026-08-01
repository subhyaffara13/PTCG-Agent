
def test_linedash():
    """Test that dashed lines do not break PS output"""
    fig, ax = plt.subplots()

    ax.plot([0, 1], linestyle="--")

    buf = io.BytesIO()
    fig.savefig(buf, format="ps")

    assert buf.tell() > 0

