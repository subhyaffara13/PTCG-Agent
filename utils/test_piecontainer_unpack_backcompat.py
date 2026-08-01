
def test_piecontainer_unpack_backcompat():
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        [2, 3], labels=['foo', 'bar'], autopct="%1.0f%%", labeldistance=None)

    assert len(wedges) == 2
    assert isinstance(texts, list)
    assert not texts
    assert len(autotexts) == 2

