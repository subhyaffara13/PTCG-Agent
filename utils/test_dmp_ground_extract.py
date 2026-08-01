
def test_dmp_ground_extract():
    f = dmp_normal(
        [[2930944], [], [2198208], [], [549552], [], [45796]], 1, ZZ)
    g = dmp_normal([[17585664], [], [8792832], [], [1099104], []], 1, ZZ)

    F = dmp_normal([[64], [], [48], [], [12], [], [1]], 1, ZZ)
    G = dmp_normal([[384], [], [192], [], [24], []], 1, ZZ)

    assert dmp_ground_extract(f, g, 1, ZZ) == (45796, F, G)

