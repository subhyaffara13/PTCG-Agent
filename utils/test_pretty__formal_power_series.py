
def test_pretty_FormalPowerSeries():
    f = fps(log(1 + x))


    ascii_str = \
"""\
 oo              \n\
____             \n\
\\   `            \n\
 \\         -k  k \n\
  \\   -(-1)  *x  \n\
  /   -----------\n\
 /         k     \n\
/___,            \n\
k = 1            \
"""

    ucode_str = \
"""\
 ∞               \n\
____             \n\
╲                \n\
 ╲         -k  k \n\
  ╲   -(-1)  ⋅x  \n\
  ╱   ───────────\n\
 ╱         k     \n\
╱                \n\
‾‾‾‾             \n\
k = 1            \
"""

    assert pretty(f) == ascii_str
    assert upretty(f) == ucode_str

