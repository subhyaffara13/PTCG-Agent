from typing import Tuple

def test_constructor():
    # this is shared by Sum, so testing Integral's constructor
    # is equivalent to testing Sum's
    s1 = Integral(n, n)
    assert s1.limits == (Tuple(n),)
    s2 = Integral(n, (n,))
    assert s2.limits == (Tuple(n),)
    s3 = Integral(Sum(x, (x, 1, y)))
    assert s3.limits == (Tuple(y),)
    s4 = Integral(n, Tuple(n,))
    assert s4.limits == (Tuple(n),)

    s5 = Integral(n, (n, Interval(1, 2)))
    assert s5.limits == (Tuple(n, 1, 2),)

    # Testing constructor with inequalities:
    s6 = Integral(n, n > 10)
    assert s6.limits == (Tuple(n, 10, oo),)
    s7 = Integral(n, (n > 2) & (n < 5))
    assert s7.limits == (Tuple(n, 2, 5),)


def test_constructor(rand_series_with_duplicate_datetimeindex):
    dups = rand_series_with_duplicate_datetimeindex
    assert isinstance(dups, Series)
    assert isinstance(dups.index, DatetimeIndex)


def test_constructor(frame_or_series):
    c = frame_or_series(range(5)).ewm

    # valid
    c(com=0.5)
    c(span=1.5)
    c(alpha=0.5)
    c(halflife=0.75)
    c(com=0.5, span=None)
    c(alpha=0.5, com=None)
    c(halflife=0.75, alpha=None)

    # not valid: mutually exclusive
    msg = "comass, span, halflife, and alpha are mutually exclusive"
    with pytest.raises(ValueError, match=msg):
        c(com=0.5, alpha=0.5)
    with pytest.raises(ValueError, match=msg):
        c(span=1.5, halflife=0.75)
    with pytest.raises(ValueError, match=msg):
        c(alpha=0.5, span=1.5)

    # not valid: com < 0
    msg = "comass must satisfy: comass >= 0"
    with pytest.raises(ValueError, match=msg):
        c(com=-0.5)

    # not valid: span < 1
    msg = "span must satisfy: span >= 1"
    with pytest.raises(ValueError, match=msg):
        c(span=0.5)

    # not valid: halflife <= 0
    msg = "halflife must satisfy: halflife > 0"
    with pytest.raises(ValueError, match=msg):
        c(halflife=0)

    # not valid: alpha <= 0 or alpha > 1
    msg = "alpha must satisfy: 0 < alpha <= 1"
    for alpha in (-0.5, 1.5):
        with pytest.raises(ValueError, match=msg):
            c(alpha=alpha)


def test_constructor(frame_or_series):
    # GH 12669

    c = frame_or_series(range(5)).expanding

    # valid
    c(min_periods=1)


def test_constructor(frame_or_series):
    # GH 12669

    c = frame_or_series(range(5)).rolling

    # valid
    c(0)
    c(window=2)
    c(window=2, min_periods=1)
    c(window=2, min_periods=1, center=True)
    c(window=2, min_periods=1, center=False)

    # GH 13383

    msg = "window must be an integer 0 or greater"

    with pytest.raises(ValueError, match=msg):
        c(-1)


def test_constructor(frame_or_series):
    # GH 12669
    pytest.importorskip("scipy")
    c = frame_or_series(range(5)).rolling

    # valid
    c(win_type="boxcar", window=2, min_periods=1)
    c(win_type="boxcar", window=2, min_periods=1, center=True)
    c(win_type="boxcar", window=2, min_periods=1, center=False)

