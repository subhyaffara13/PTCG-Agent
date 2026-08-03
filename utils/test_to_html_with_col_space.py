import re

def test_to_html_with_col_space(col_space):
    df = DataFrame(np.random.default_rng(2).random(size=(1, 3)))
    # check that col_space affects HTML generation
    # and be very brittle about it.
    result = df.to_html(col_space=col_space)
    hdrs = [x for x in result.split(r"\n") if re.search(r"<th[>\s]", x)]
    assert len(hdrs) > 0
    for h in hdrs:
        assert "min-width" in h
        assert str(col_space) in h

