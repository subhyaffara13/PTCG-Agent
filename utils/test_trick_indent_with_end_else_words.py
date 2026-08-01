
def test_trick_indent_with_end_else_words():
    # words starting with "end" or "else" do not confuse the indenter
    t1 = S('endless')
    t2 = S('elsewhere')
    pw = Piecewise((t1, x < 0), (t2, x <= 1), (1, True))
    assert julia_code(pw, inline=False) == (
        "if (x < 0)\n"
        "    endless\n"
        "elseif (x <= 1)\n"
        "    elsewhere\n"
        "else\n"
        "    1\n"
        "end")


def test_trick_indent_with_end_else_words():
    # words starting with "end" or "else" do not confuse the indenter
    t1 = S('endless')
    t2 = S('elsewhere')
    pw = Piecewise((t1, x < 0), (t2, x <= 1), (1, True))
    assert mcode(pw, inline=False) == (
        "if (x < 0)\n"
        "  endless\n"
        "elseif (x <= 1)\n"
        "  elsewhere\n"
        "else\n"
        "  1\n"
        "end")

