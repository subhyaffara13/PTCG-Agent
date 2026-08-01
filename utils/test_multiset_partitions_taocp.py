
def test_multiset_partitions_taocp():
    """Compares the output of multiset_partitions_taocp with a baseline
    (set partition based) implementation."""

    # Test cases should not be too large, since the baseline
    # implementation is fairly slow.
    multiplicities = [2,2]
    compare_multiset_w_baseline(multiplicities)

    multiplicities = [4,3,1]
    compare_multiset_w_baseline(multiplicities)

