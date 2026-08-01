
def test_kbins():
    assert len(list(kbins('1123', 2, ordered=1))) == 24
    assert len(list(kbins('1123', 2, ordered=11))) == 36
    assert len(list(kbins('1123', 2, ordered=10))) == 10
    assert len(list(kbins('1123', 2, ordered=0))) == 5
    assert len(list(kbins('1123', 2, ordered=None))) == 3

    def test1():
        for orderedval in [None, 0, 1, 10, 11]:
            print('ordered =', orderedval)
            for p in kbins([0, 0, 1], 2, ordered=orderedval):
                print('   ', p)
    assert capture(lambda : test1()) == dedent('''\
        ordered = None
            [[0], [0, 1]]
            [[0, 0], [1]]
        ordered = 0
            [[0, 0], [1]]
            [[0, 1], [0]]
        ordered = 1
            [[0], [0, 1]]
            [[0], [1, 0]]
            [[1], [0, 0]]
        ordered = 10
            [[0, 0], [1]]
            [[1], [0, 0]]
            [[0, 1], [0]]
            [[0], [0, 1]]
        ordered = 11
            [[0], [0, 1]]
            [[0, 0], [1]]
            [[0], [1, 0]]
            [[0, 1], [0]]
            [[1], [0, 0]]
            [[1, 0], [0]]\n''')

    def test2():
        for orderedval in [None, 0, 1, 10, 11]:
            print('ordered =', orderedval)
            for p in kbins(list(range(3)), 2, ordered=orderedval):
                print('   ', p)
    assert capture(lambda : test2()) == dedent('''\
        ordered = None
            [[0], [1, 2]]
            [[0, 1], [2]]
        ordered = 0
            [[0, 1], [2]]
            [[0, 2], [1]]
            [[0], [1, 2]]
        ordered = 1
            [[0], [1, 2]]
            [[0], [2, 1]]
            [[1], [0, 2]]
            [[1], [2, 0]]
            [[2], [0, 1]]
            [[2], [1, 0]]
        ordered = 10
            [[0, 1], [2]]
            [[2], [0, 1]]
            [[0, 2], [1]]
            [[1], [0, 2]]
            [[0], [1, 2]]
            [[1, 2], [0]]
        ordered = 11
            [[0], [1, 2]]
            [[0, 1], [2]]
            [[0], [2, 1]]
            [[0, 2], [1]]
            [[1], [0, 2]]
            [[1, 0], [2]]
            [[1], [2, 0]]
            [[1, 2], [0]]
            [[2], [0, 1]]
            [[2, 0], [1]]
            [[2], [1, 0]]
            [[2, 1], [0]]\n''')

