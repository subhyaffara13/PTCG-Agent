
def compare_multiset_w_baseline(multiplicities):
    """
    Enumerates the partitions of multiset with AOCP algorithm and
    baseline implementation, and compare the results.

    """
    letters = string.ascii_lowercase
    bl_partitions = multiset_partitions_baseline(multiplicities, letters)

    # The partitions returned by the different algorithms may have
    # their parts in different orders.  Also, they generate partitions
    # in different orders.  Hence the sorting, and set comparison.

    aocp_partitions = set()
    for state in multiset_partitions_taocp(multiplicities):
        p1 = tuple(sorted(
                [tuple(p) for p in list_visitor(state, letters)]))
        aocp_partitions.add(p1)

    assert bl_partitions == aocp_partitions

