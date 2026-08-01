
def axis_test(axis, labels):
    ticks = list(range(len(labels)))
    np.testing.assert_array_equal(axis.get_majorticklocs(), ticks)
    graph_labels = [axis.major.formatter(i, i) for i in ticks]
    # _text also decodes bytes as utf-8.
    assert graph_labels == [cat.StrCategoryFormatter._text(l) for l in labels]
    assert list(axis.units._mapping.keys()) == [l for l in labels]
    assert list(axis.units._mapping.values()) == ticks

