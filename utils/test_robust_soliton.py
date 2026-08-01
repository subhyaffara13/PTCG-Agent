
def test_robust_soliton():
    raises(ValueError, lambda : RobustSoliton('robSol', -12, 0.1, 0.02))
    raises(ValueError, lambda : RobustSoliton('robSol', 13, 1.89, 0.1))
    raises(ValueError, lambda : RobustSoliton('robSol', 15, 0.6, -2.31))
    f = Function('f')
    raises(ValueError, lambda : density(RobustSoliton('robSol', 15, 0.6, 0.1)).pmf(f))

    k = Symbol('k', integer=True, positive=True)
    delta = Symbol('delta', positive=True)
    c = Symbol('c', positive=True)
    robSol = RobustSoliton('robSol', k, delta, c)
    assert density(robSol).low == 1
    assert density(robSol).high == k

    k_vals = [10, 20, 50]
    delta_vals = [0.2, 0.4, 0.6]
    c_vals = [0.01, 0.03, 0.05]
    for x in k_vals:
        for y in delta_vals:
            for z in c_vals:
                assert E(robSol.subs({k: x, delta: y, c: z})) == moment(robSol.subs({k: x, delta: y, c: z}), 1)
                assert variance(robSol.subs({k: x, delta: y, c: z})) == cmoment(robSol.subs({k: x, delta: y, c: z}), 2)
                assert skewness(robSol.subs({k: x, delta: y, c: z})) == smoment(robSol.subs({k: x, delta: y, c: z}), 3)
                assert kurtosis(robSol.subs({k: x, delta: y, c: z})) == smoment(robSol.subs({k: x, delta: y, c: z}), 4)

