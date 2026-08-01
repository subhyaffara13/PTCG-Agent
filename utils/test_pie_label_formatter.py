
def test_pie_label_formatter():
    fig, ax = plt.subplots()
    pie = ax.pie([2, 3])

    texts = ax.pie_label(pie, '{absval:03d}')
    assert texts[0].get_text() == '002'
    assert texts[1].get_text() == '003'

    texts = ax.pie_label(pie, '{frac:.1%}')
    assert texts[0].get_text() == '40.0%'
    assert texts[1].get_text() == '60.0%'

