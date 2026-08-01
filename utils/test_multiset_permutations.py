
def test_multiset_permutations():
    ans = ['abby', 'abyb', 'aybb', 'baby', 'bayb', 'bbay', 'bbya', 'byab',
           'byba', 'yabb', 'ybab', 'ybba']
    assert [''.join(i) for i in multiset_permutations('baby')] == ans
    assert [''.join(i) for i in multiset_permutations(multiset('baby'))] == ans
    assert list(multiset_permutations([0, 0, 0], 2)) == [[0, 0]]
    assert list(multiset_permutations([0, 2, 1], 2)) == [
        [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1]]
    assert len(list(multiset_permutations('a', 0))) == 1
    assert len(list(multiset_permutations('a', 3))) == 0
    for nul in ([], {}, ''):
        assert list(multiset_permutations(nul)) == [[]]
    assert list(multiset_permutations(nul, 0)) == [[]]
    # impossible requests give no result
    assert list(multiset_permutations(nul, 1)) == []
    assert list(multiset_permutations(nul, -1)) == []

    def test():
        for i in range(1, 7):
            print(i)
            for p in multiset_permutations([0, 0, 1, 0, 1], i):
                print(p)
    assert capture(lambda: test()) == dedent('''\
        1
        [0]
        [1]
        2
        [0, 0]
        [0, 1]
        [1, 0]
        [1, 1]
        3
        [0, 0, 0]
        [0, 0, 1]
        [0, 1, 0]
        [0, 1, 1]
        [1, 0, 0]
        [1, 0, 1]
        [1, 1, 0]
        4
        [0, 0, 0, 1]
        [0, 0, 1, 0]
        [0, 0, 1, 1]
        [0, 1, 0, 0]
        [0, 1, 0, 1]
        [0, 1, 1, 0]
        [1, 0, 0, 0]
        [1, 0, 0, 1]
        [1, 0, 1, 0]
        [1, 1, 0, 0]
        5
        [0, 0, 0, 1, 1]
        [0, 0, 1, 0, 1]
        [0, 0, 1, 1, 0]
        [0, 1, 0, 0, 1]
        [0, 1, 0, 1, 0]
        [0, 1, 1, 0, 0]
        [1, 0, 0, 0, 1]
        [1, 0, 0, 1, 0]
        [1, 0, 1, 0, 0]
        [1, 1, 0, 0, 0]
        6\n''')
    raises(ValueError, lambda: list(multiset_permutations({0: 3, 1: -1})))

