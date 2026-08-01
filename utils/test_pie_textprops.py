
def test_pie_textprops():
    data = [23, 34, 45]
    labels = ["Long name 1", "Long name 2", "Long name 3"]

    textprops = dict(horizontalalignment="center",
                     verticalalignment="top",
                     rotation=90,
                     rotation_mode="anchor",
                     size=12, color="red")

    _, texts, autopct = plt.gca().pie(data, labels=labels, autopct='%.2f',
                                      textprops=textprops)
    for labels in [texts, autopct]:
        for tx in labels:
            assert tx.get_ha() == textprops["horizontalalignment"]
            assert tx.get_va() == textprops["verticalalignment"]
            assert tx.get_rotation() == textprops["rotation"]
            assert tx.get_rotation_mode() == textprops["rotation_mode"]
            assert tx.get_size() == textprops["size"]
            assert tx.get_color() == textprops["color"]

