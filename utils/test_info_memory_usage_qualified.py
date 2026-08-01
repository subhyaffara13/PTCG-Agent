
def test_info_memory_usage_qualified(index, plus):
    buf = StringIO()
    series = Series(1, index=index)
    series.info(buf=buf)
    if plus:
        assert "+" in buf.getvalue()
    else:
        assert "+" not in buf.getvalue()


def test_info_memory_usage_qualified(using_infer_string):
    buf = StringIO()
    df = DataFrame(1, columns=list("ab"), index=[1, 2, 3])
    df.info(buf=buf)
    assert "+" not in buf.getvalue()

    buf = StringIO()
    df = DataFrame(1, columns=list("ab"), index=Index(list("ABC"), dtype=object))
    df.info(buf=buf)
    assert "+" in buf.getvalue()

    buf = StringIO()
    df = DataFrame(1, columns=list("ab"), index=Index(list("ABC"), dtype="str"))
    df.info(buf=buf)
    if using_infer_string and HAS_PYARROW:
        assert "+" not in buf.getvalue()
    else:
        assert "+" in buf.getvalue()

    buf = StringIO()
    df = DataFrame(
        1, columns=list("ab"), index=MultiIndex.from_product([range(3), range(3)])
    )
    df.info(buf=buf)
    assert "+" not in buf.getvalue()

    buf = StringIO()
    df = DataFrame(
        1, columns=list("ab"), index=MultiIndex.from_product([range(3), ["foo", "bar"]])
    )
    df.info(buf=buf)
    if using_infer_string and HAS_PYARROW:
        assert "+" not in buf.getvalue()
    else:
        assert "+" in buf.getvalue()

