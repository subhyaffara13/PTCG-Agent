
def test_info_verbose_check_header_separator_body():
    buf = StringIO()
    size = 1001
    start = 5
    frame = DataFrame(np.random.default_rng(2).standard_normal((3, size)))
    frame.info(verbose=True, buf=buf)

    res = buf.getvalue()
    header = " #     Column  Dtype  \n---    ------  -----  "
    assert header in res

    frame.info(verbose=True, buf=buf)
    buf.seek(0)
    lines = buf.readlines()
    assert len(lines) > 0

    for i, line in enumerate(lines):
        if start <= i < start + size:
            line_nr = f" {i - start} "
            assert line.startswith(line_nr)

