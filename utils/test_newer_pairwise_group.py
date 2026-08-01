
def test_newer_pairwise_group(groups_target):
    older = newer_pairwise_group([groups_target.older], [groups_target.target])
    newer = newer_pairwise_group([groups_target.newer], [groups_target.target])
    assert older == ([], [])
    assert newer == ([groups_target.newer], [groups_target.target])

