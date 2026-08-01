
def test_partitions():
    ans = [[{}], [(0, {})]]
    for i in range(2):
        assert list(partitions(0, size=i)) == ans[i]
        assert list(partitions(1, 0, size=i)) == ans[i]
        assert list(partitions(6, 2, 2, size=i)) == ans[i]
        assert list(partitions(6, 2, None, size=i)) != ans[i]
        assert list(partitions(6, None, 2, size=i)) != ans[i]
        assert list(partitions(6, 2, 0, size=i)) == ans[i]

    assert list(partitions(6, k=2)) == [
        {2: 3}, {1: 2, 2: 2}, {1: 4, 2: 1}, {1: 6}]

    assert list(partitions(6, k=3)) == [
        {3: 2}, {1: 1, 2: 1, 3: 1}, {1: 3, 3: 1}, {2: 3}, {1: 2, 2: 2},
        {1: 4, 2: 1}, {1: 6}]

    assert list(partitions(8, k=4, m=3)) == [
        {4: 2}, {1: 1, 3: 1, 4: 1}, {2: 2, 4: 1}, {2: 1, 3: 2}] == [
        i for i in partitions(8, k=4, m=3) if all(k <= 4 for k in i)
        and sum(i.values()) <=3]

    assert list(partitions(S(3), m=2)) == [
        {3: 1}, {1: 1, 2: 1}]

    assert list(partitions(4, k=3)) == [
        {1: 1, 3: 1}, {2: 2}, {1: 2, 2: 1}, {1: 4}] == [
        i for i in partitions(4) if all(k <= 3 for k in i)]


    # Consistency check on output of _partitions and RGS_unrank.
    # This provides a sanity test on both routines.  Also verifies that
    # the total number of partitions is the same in each case.
    #    (from pkrathmann2)

    for n in range(2, 6):
        i  = 0
        for m, q  in _set_partitions(n):
            assert  q == RGS_unrank(i, n)
            i += 1
        assert i == RGS_enum(n)

