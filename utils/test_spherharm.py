
def test_spherharm():
    mp.dps = 15
    t = 0.5; r = 0.25
    assert spherharm(0,0,t,r).ae(0.28209479177387814347)
    assert spherharm(1,-1,t,r).ae(0.16048941205971996369 - 0.04097967481096344271j)
    assert spherharm(1,0,t,r).ae(0.42878904414183579379)
    assert spherharm(1,1,t,r).ae(-0.16048941205971996369 - 0.04097967481096344271j)
    assert spherharm(2,-2,t,r).ae(0.077915886919031181734 - 0.042565643022253962264j)
    assert spherharm(2,-1,t,r).ae(0.31493387233497459884 - 0.08041582001959297689j)
    assert spherharm(2,0,t,r).ae(0.41330596756220761898)
    assert spherharm(2,1,t,r).ae(-0.31493387233497459884 - 0.08041582001959297689j)
    assert spherharm(2,2,t,r).ae(0.077915886919031181734 + 0.042565643022253962264j)
    assert spherharm(3,-3,t,r).ae(0.033640236589690881646 - 0.031339125318637082197j)
    assert spherharm(3,-2,t,r).ae(0.18091018743101461963 - 0.09883168583167010241j)
    assert spherharm(3,-1,t,r).ae(0.42796713930907320351 - 0.10927795157064962317j)
    assert spherharm(3,0,t,r).ae(0.27861659336351639787)
    assert spherharm(3,1,t,r).ae(-0.42796713930907320351 - 0.10927795157064962317j)
    assert spherharm(3,2,t,r).ae(0.18091018743101461963 + 0.09883168583167010241j)
    assert spherharm(3,3,t,r).ae(-0.033640236589690881646 - 0.031339125318637082197j)
    assert spherharm(0,-1,t,r) == 0
    assert spherharm(0,-2,t,r) == 0
    assert spherharm(0,1,t,r) == 0
    assert spherharm(0,2,t,r) == 0
    assert spherharm(1,2,t,r) == 0
    assert spherharm(1,3,t,r) == 0
    assert spherharm(1,-2,t,r) == 0
    assert spherharm(1,-3,t,r) == 0
    assert spherharm(2,3,t,r) == 0
    assert spherharm(2,4,t,r) == 0
    assert spherharm(2,-3,t,r) == 0
    assert spherharm(2,-4,t,r) == 0
    assert spherharm(3,4.5,0.5,0.25).ae(-22.831053442240790148 + 10.910526059510013757j)
    assert spherharm(2+3j, 1-j, 1+j, 3+4j).ae(-2.6582752037810116935 - 1.0909214905642160211j)
    assert spherharm(-6,2.5,t,r).ae(0.39383644983851448178 + 0.28414687085358299021j)
    assert spherharm(-3.5, 3, 0.5, 0.25).ae(0.014516852987544698924 - 0.015582769591477628495j)
    assert spherharm(-3, 3, 0.5, 0.25) == 0
    assert spherharm(-6, 3, 0.5, 0.25).ae(-0.16544349818782275459 - 0.15412657723253924562j)
    assert spherharm(-6, 1.5, 0.5, 0.25).ae(0.032208193499767402477 + 0.012678000924063664921j)
    assert spherharm(3,0,0,1).ae(0.74635266518023078283)
    assert spherharm(3,-2,0,1) == 0
    assert spherharm(3,-2,1,1).ae(-0.16270707338254028971 - 0.35552144137546777097j)

