
def test_fitstart(distname, shapes):
    dist = getattr(stats, distname)
    rng = np.random.default_rng(216342614)
    data = rng.random(10)

    with np.errstate(invalid='ignore', divide='ignore'):  # irrelevant to test
        guess = dist._fitstart(data)

    assert dist._argcheck(*guess[:-2])

