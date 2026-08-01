
def test_print_polylog_long_order_issue_25309():
    s, z = symbols("s, z")
    ucode_str = \
"""\
       ⎛ 2   ⎞\n\
polylog⎝s , z⎠\
"""
    assert upretty(polylog(s**2, z)) == ucode_str

