
def check_onetree_query(T, d):
    r = T.query_ball_tree(T, d)
    s = set()
    for i, l in enumerate(r):
        for j in l:
            if i < j:
                s.add((i, j))

    assert_(s == T.query_pairs(d))

