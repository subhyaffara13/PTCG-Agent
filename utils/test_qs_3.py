
def test_qs_3():
    N = 1817
    smooth_relations = [
        (2455024, 637, 8),
        (-27993000, 81536, 10),
        (11461840, 12544, 0),
        (149, 20384, 10),
        (-31138074, 19208, 2)
    ]
    assert next(_find_factor(N, smooth_relations, 4)) == 23

