
def test_issue_7927():
    e = sin(x/2)**cos(x/2)
    ucode_str = \
"""\
           ⎛x⎞\n\
        cos⎜─⎟\n\
           ⎝2⎠\n\
⎛   ⎛x⎞⎞      \n\
⎜sin⎜─⎟⎟      \n\
⎝   ⎝2⎠⎠      \
"""
    assert upretty(e) == ucode_str
    e = sin(x)**(S(11)/13)
    ucode_str = \
"""\
        11\n\
        ──\n\
        13\n\
(sin(x))  \
"""
    assert upretty(e) == ucode_str

