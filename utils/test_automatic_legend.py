
def test_automatic_legend():
    fig, ax = plt.subplots()
    ax.plot("a", "b", data={"d": 2})
    leg = ax.legend()
    fig.canvas.draw()
    assert leg.get_texts()[0].get_text() == 'a'
    assert ax.get_yticklabels()[0].get_text() == 'a'

    fig, ax = plt.subplots()
    ax.plot("a", "b", "c", data={"d": 2})
    leg = ax.legend()
    fig.canvas.draw()
    assert leg.get_texts()[0].get_text() == 'b'
    assert ax.get_xticklabels()[0].get_text() == 'a'
    assert ax.get_yticklabels()[0].get_text() == 'b'

