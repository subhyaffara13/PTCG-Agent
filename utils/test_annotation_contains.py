
def test_annotation_contains():
    # Check that Annotation.contains looks at the bboxes of the text and the
    # arrow separately, not at the joint bbox.
    fig, ax = plt.subplots()
    ann = ax.annotate(
        "hello", xy=(.4, .4), xytext=(.6, .6), arrowprops={"arrowstyle": "->"})
    fig.canvas.draw()  # Needed for the same reason as in test_contains.
    event = MouseEvent(
        "button_press_event", fig.canvas, *ax.transData.transform((.5, .6)))
    assert ann.contains(event) == (False, {})

