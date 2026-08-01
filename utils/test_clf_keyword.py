
def test_clf_keyword():
    # test if existing figure is cleared with figure() and subplots()
    text1 = 'A fancy plot'
    text2 = 'Really fancy!'

    fig0 = plt.figure(num=1)
    fig0.suptitle(text1)
    assert [t.get_text() for t in fig0.texts] == [text1]

    fig1 = plt.figure(num=1, clear=False)
    fig1.text(0.5, 0.5, text2)
    assert fig0 is fig1
    assert [t.get_text() for t in fig1.texts] == [text1, text2]

    fig2, ax2 = plt.subplots(2, 1, num=1, clear=True)
    assert fig0 is fig2
    assert [t.get_text() for t in fig2.texts] == []

