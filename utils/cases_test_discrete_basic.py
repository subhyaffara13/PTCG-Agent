
def cases_test_discrete_basic():
    seen = set()
    for distname, arg in distdiscrete:
        if distname in distslow:
            yield pytest.param(distname, arg, distname, marks=pytest.mark.slow)
        else:
            yield distname, arg, distname not in seen
        seen.add(distname)

