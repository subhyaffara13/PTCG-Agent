
def test_annotate_signature():
    """Check that the signature of Axes.annotate() matches Annotation."""
    fig, ax = plt.subplots()
    annotate_params = inspect.signature(ax.annotate).parameters
    annotation_params = inspect.signature(mtext.Annotation).parameters
    assert list(annotate_params.keys()) == list(annotation_params.keys())
    for p1, p2 in zip(annotate_params.values(), annotation_params.values()):
        assert p1 == p2

