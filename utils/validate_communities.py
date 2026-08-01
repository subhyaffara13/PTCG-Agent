
def validate_communities(result, expected):
    assert set_of_sets(result) == set_of_sets(expected)

