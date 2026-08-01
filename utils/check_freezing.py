
def check_freezing(distfn, args):
    # regression test for gh-11089: freezing a distribution fails
    # if loc and/or scale are specified
    if isinstance(distfn, stats.rv_continuous):
        locscale = {'loc': 1, 'scale': 2}
    else:
        locscale = {'loc': 1}

    rv = distfn(*args, **locscale)
    assert rv.a == distfn(*args).a
    assert rv.b == distfn(*args).b

