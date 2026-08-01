
def test_TableForm():
    s = str(TableForm([["a", "b"], ["c", "d"], ["e", 0]],
        headings="automatic"))
    assert s == (
        '  | 1 2\n'
        '-------\n'
        '1 | a b\n'
        '2 | c d\n'
        '3 | e  '
    )
    s = str(TableForm([["a", "b"], ["c", "d"], ["e", 0]],
        headings="automatic", wipe_zeros=False))
    assert s == dedent('''\
          | 1 2
        -------
        1 | a b
        2 | c d
        3 | e 0''')
    s = str(TableForm([[x**2, "b"], ["c", x**2], ["e", "f"]],
            headings=("automatic", None)))
    assert s == (
        '1 | x**2 b   \n'
        '2 | c    x**2\n'
        '3 | e    f   '
    )
    s = str(TableForm([["a", "b"], ["c", "d"], ["e", "f"]],
            headings=(None, "automatic")))
    assert s == dedent('''\
        1 2
        ---
        a b
        c d
        e f''')
    s = str(TableForm([[5, 7], [4, 2], [10, 3]],
            headings=[["Group A", "Group B", "Group C"], ["y1", "y2"]]))
    assert s == (
        '        | y1 y2\n'
        '---------------\n'
        'Group A | 5  7 \n'
        'Group B | 4  2 \n'
        'Group C | 10 3 '
    )
    raises(
        ValueError,
        lambda:
        TableForm(
            [[5, 7], [4, 2], [10, 3]],
            headings=[["Group A", "Group B", "Group C"], ["y1", "y2"]],
            alignments="middle")
    )
    s = str(TableForm([[5, 7], [4, 2], [10, 3]],
            headings=[["Group A", "Group B", "Group C"], ["y1", "y2"]],
            alignments="right"))
    assert s == dedent('''\
                | y1 y2
        ---------------
        Group A |  5  7
        Group B |  4  2
        Group C | 10  3''')

    # other alignment permutations
    d = [[1, 100], [100, 1]]
    s = TableForm(d, headings=(('xxx', 'x'), None), alignments='l')
    assert str(s) == (
        'xxx | 1   100\n'
        '  x | 100 1  '
    )
    s = TableForm(d, headings=(('xxx', 'x'), None), alignments='lr')
    assert str(s) == dedent('''\
    xxx | 1   100
      x | 100   1''')
    s = TableForm(d, headings=(('xxx', 'x'), None), alignments='clr')
    assert str(s) == dedent('''\
    xxx | 1   100
     x  | 100   1''')

    s = TableForm(d, headings=(('xxx', 'x'), None))
    assert str(s) == (
        'xxx | 1   100\n'
        '  x | 100 1  '
    )

    raises(ValueError, lambda: TableForm(d, alignments='clr'))

    #pad
    s = str(TableForm([[None, "-", 2], [1]], pad='?'))
    assert s == dedent('''\
        ? - 2
        1 ? ?''')

