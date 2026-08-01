
def test_info_categorical():
    # GH14298
    idx = CategoricalIndex(["a", "b"])
    s = Series(np.zeros(2), index=idx)
    buf = StringIO()
    s.info(buf=buf)


def test_info_categorical():
    # GH14298
    idx = CategoricalIndex(["a", "b"])
    df = DataFrame(np.zeros((2, 2)), index=idx, columns=idx)

    buf = StringIO()
    df.info(buf=buf)

