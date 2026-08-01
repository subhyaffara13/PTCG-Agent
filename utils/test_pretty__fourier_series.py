
def test_pretty_FourierSeries():
    f = fourier_series(x, (x, -pi, pi))

    ascii_str = \
"""\
                      2*sin(3*x)      \n\
2*sin(x) - sin(2*x) + ---------- + ...\n\
                          3           \
"""

    ucode_str = \
"""\
                      2⋅sin(3⋅x)    \n\
2⋅sin(x) - sin(2⋅x) + ────────── + …\n\
                          3         \
"""

    assert pretty(f) == ascii_str
    assert upretty(f) == ucode_str

