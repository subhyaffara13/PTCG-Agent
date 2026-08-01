
def test_aligned():
    if hasattr(m, "Aligned"):
        p = m.Aligned().ptr()
        assert p % 1024 == 0

