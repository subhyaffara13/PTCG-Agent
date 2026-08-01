
def _check_text_labels(texts, expected):
    """
    Check each text has expected labels

    Parameters
    ----------
    texts : matplotlib Text object, or its list-like
        target text, or its list
    expected : str or list-like which has the same length as texts
        expected text label, or its list
    """
    if not is_list_like(texts):
        assert texts.get_text() == expected
    else:
        labels = [t.get_text() for t in texts]
        assert len(labels) == len(expected)
        for label, e in zip(labels, expected, strict=True):
            assert label == e

