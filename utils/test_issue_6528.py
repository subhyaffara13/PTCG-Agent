
def test_issue_6528():
    eqs = [
        327600995*x**2 - 37869137*x + 1809975124*y**2 - 9998905626,
        895613949*x**2 - 273830224*x*y + 530506983*y**2 - 10000000000]
    # two expressions encountered are > 1400 ops long so if this hangs
    # it is likely because simplification is being done
    assert len(solve(eqs, y, x, check=False)) == 4

