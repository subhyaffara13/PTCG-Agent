
def test_hatching_legend(text_placeholders):
    """Test for correct hatching on patches in legend"""
    fig = plt.figure(figsize=(1, 2))

    a = Rectangle([0, 0], 0, 0, facecolor="green", hatch="XXXX")
    b = Rectangle([0, 0], 0, 0, facecolor="blue", hatch="XXXX")

    # Verify that hatches in PDFs work after empty labels. See
    # https://github.com/matplotlib/matplotlib/issues/4469
    fig.legend([a, b, a, b], ["", "", "", ""])

