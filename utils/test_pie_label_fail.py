import re

def test_pie_label_fail():
    sizes = 15, 30, 45, 10
    labels = 'Frogs', 'Hogs'
    fig, ax = plt.subplots()
    pie = ax.pie(sizes)

    match = re.escape("The number of labels (2) must match the number of wedges (4)")
    with pytest.raises(ValueError, match=match):
        ax.pie_label(pie, labels)

