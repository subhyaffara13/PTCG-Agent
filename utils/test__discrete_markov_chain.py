from typing import Tuple

def test_DiscreteMarkovChain():

    # pass only the name
    X = DiscreteMarkovChain("X")
    assert isinstance(X.state_space, Range)
    assert X.index_set == S.Naturals0
    assert isinstance(X.transition_probabilities, MatrixSymbol)
    t = symbols('t', positive=True, integer=True)
    assert isinstance(X[t], RandomIndexedSymbol)
    assert E(X[0]) == Expectation(X[0])
    raises(TypeError, lambda: DiscreteMarkovChain(1))
    raises(NotImplementedError, lambda: X(t))
    raises(NotImplementedError, lambda: X.communication_classes())
    raises(NotImplementedError, lambda: X.canonical_form())
    raises(NotImplementedError, lambda: X.decompose())

    nz = Symbol('n', integer=True)
    TZ = MatrixSymbol('M', nz, nz)
    SZ = Range(nz)
    YZ = DiscreteMarkovChain('Y', SZ, TZ)
    assert P(Eq(YZ[2], 1), Eq(YZ[1], 0)) == TZ[0, 1]

    raises(ValueError, lambda: sample_stochastic_process(t))
    raises(ValueError, lambda: next(sample_stochastic_process(X)))
    # pass name and state_space
    # any hashable object should be a valid state
    # states should be valid as a tuple/set/list/Tuple/Range
    sym, rainy, cloudy, sunny = symbols('a Rainy Cloudy Sunny', real=True)
    state_spaces = [(1, 2, 3), [Str('Hello'), sym, DiscreteMarkovChain("Y", (1,2,3))],
                    Tuple(S(1), exp(sym), Str('World'), sympify=False), Range(-1, 5, 2),
                    [rainy, cloudy, sunny]]
    chains = [DiscreteMarkovChain("Y", state_space) for state_space in state_spaces]

    for i, Y in enumerate(chains):
        assert isinstance(Y.transition_probabilities, MatrixSymbol)
        assert Y.state_space == state_spaces[i] or Y.state_space == FiniteSet(*state_spaces[i])
        assert Y.number_of_states == 3

        with ignore_warnings(UserWarning):  # TODO: Restore tests once warnings are removed
            assert P(Eq(Y[2], 1), Eq(Y[0], 2), evaluate=False) == Probability(Eq(Y[2], 1), Eq(Y[0], 2))
        assert E(Y[0]) == Expectation(Y[0])

        raises(ValueError, lambda: next(sample_stochastic_process(Y)))

    raises(TypeError, lambda: DiscreteMarkovChain("Y", {1: 1}))
    Y = DiscreteMarkovChain("Y", Range(1, t, 2))
    assert Y.number_of_states == ceiling((t-1)/2)

    # pass name and transition_probabilities
    chains = [DiscreteMarkovChain("Y", trans_probs=Matrix([])),
              DiscreteMarkovChain("Y", trans_probs=Matrix([[0, 1], [1, 0]])),
              DiscreteMarkovChain("Y", trans_probs=Matrix([[pi, 1-pi], [sym, 1-sym]]))]
    for Z in chains:
        assert Z.number_of_states == Z.transition_probabilities.shape[0]
        assert isinstance(Z.transition_probabilities, ImmutableMatrix)

    # pass name, state_space and transition_probabilities
    T = Matrix([[0.5, 0.2, 0.3],[0.2, 0.5, 0.3],[0.2, 0.3, 0.5]])
    TS = MatrixSymbol('T', 3, 3)
    Y = DiscreteMarkovChain("Y", [0, 1, 2], T)
    YS = DiscreteMarkovChain("Y", ['One', 'Two', 3], TS)
    assert Y.joint_distribution(1, Y[2], 3) == JointDistribution(Y[1], Y[2], Y[3])
    raises(ValueError, lambda: Y.joint_distribution(Y[1].symbol, Y[2].symbol))
    assert P(Eq(Y[3], 2), Eq(Y[1], 1)).round(2) == Float(0.36, 2)
    assert (P(Eq(YS[3], 2), Eq(YS[1], 1)) -
            (TS[0, 2]*TS[1, 0] + TS[1, 1]*TS[1, 2] + TS[1, 2]*TS[2, 2])).simplify() == 0
    assert P(Eq(YS[1], 1), Eq(YS[2], 2)) == Probability(Eq(YS[1], 1))
    assert P(Eq(YS[3], 3), Eq(YS[1], 1)) == TS[0, 2]*TS[1, 0] + TS[1, 1]*TS[1, 2] + TS[1, 2]*TS[2, 2]
    TO = Matrix([[0.25, 0.75, 0],[0, 0.25, 0.75],[0.75, 0, 0.25]])
    assert P(Eq(Y[3], 2), Eq(Y[1], 1) & TransitionMatrixOf(Y, TO)).round(3) == Float(0.375, 3)
    with ignore_warnings(UserWarning): ### TODO: Restore tests once warnings are removed
        assert E(Y[3], evaluate=False) == Expectation(Y[3])
        assert E(Y[3], Eq(Y[2], 1)).round(2) == Float(1.1, 3)
    TSO = MatrixSymbol('T', 4, 4)
    raises(ValueError, lambda: str(P(Eq(YS[3], 2), Eq(YS[1], 1) & TransitionMatrixOf(YS, TSO))))
    raises(TypeError, lambda: DiscreteMarkovChain("Z", [0, 1, 2], symbols('M')))
    raises(ValueError, lambda: DiscreteMarkovChain("Z", [0, 1, 2], MatrixSymbol('T', 3, 4)))
    raises(ValueError, lambda: E(Y[3], Eq(Y[2], 6)))
    raises(ValueError, lambda: E(Y[2], Eq(Y[3], 1)))


    # extended tests for probability queries
    TO1 = Matrix([[Rational(1, 4), Rational(3, 4), 0],[Rational(1, 3), Rational(1, 3), Rational(1, 3)],[0, Rational(1, 4), Rational(3, 4)]])
    assert P(And(Eq(Y[2], 1), Eq(Y[1], 1), Eq(Y[0], 0)),
            Eq(Probability(Eq(Y[0], 0)), Rational(1, 4)) & TransitionMatrixOf(Y, TO1)) == Rational(1, 16)
    assert P(And(Eq(Y[2], 1), Eq(Y[1], 1), Eq(Y[0], 0)), TransitionMatrixOf(Y, TO1)) == \
            Probability(Eq(Y[0], 0))/4
    assert P(Lt(X[1], 2) & Gt(X[1], 0), Eq(X[0], 2) &
        StochasticStateSpaceOf(X, [0, 1, 2]) & TransitionMatrixOf(X, TO1)) == Rational(1, 4)
    assert P(Lt(X[1], 2) & Gt(X[1], 0), Eq(X[0], 2) &
             StochasticStateSpaceOf(X, [S(0), '0', 1]) & TransitionMatrixOf(X, TO1)) == Rational(1, 4)
    assert P(Ne(X[1], 2) & Ne(X[1], 1), Eq(X[0], 2) &
        StochasticStateSpaceOf(X, [0, 1, 2]) & TransitionMatrixOf(X, TO1)) is S.Zero
    assert P(Ne(X[1], 2) & Ne(X[1], 1), Eq(X[0], 2) &
             StochasticStateSpaceOf(X, [S(0), '0', 1]) & TransitionMatrixOf(X, TO1)) is S.Zero
    assert P(And(Eq(Y[2], 1), Eq(Y[1], 1), Eq(Y[0], 0)), Eq(Y[1], 1)) == 0.1*Probability(Eq(Y[0], 0))

    # testing properties of Markov chain
    TO2 = Matrix([[S.One, 0, 0],[Rational(1, 3), Rational(1, 3), Rational(1, 3)],[0, Rational(1, 4), Rational(3, 4)]])
    TO3 = Matrix([[Rational(1, 4), Rational(3, 4), 0],[Rational(1, 3), Rational(1, 3), Rational(1, 3)], [0, Rational(1, 4), Rational(3, 4)]])
    Y2 = DiscreteMarkovChain('Y', trans_probs=TO2)
    Y3 = DiscreteMarkovChain('Y', trans_probs=TO3)
    assert Y3.fundamental_matrix() == ImmutableMatrix([[176, 81, -132], [36, 141, -52], [-44, -39, 208]])/125
    assert Y2.is_absorbing_chain() == True
    assert Y3.is_absorbing_chain() == False
    assert Y2.canonical_form() == ([0, 1, 2], TO2)
    assert Y3.canonical_form() == ([0, 1, 2], TO3)
    assert Y2.decompose() == ([0, 1, 2], TO2[0:1, 0:1], TO2[1:3, 0:1], TO2[1:3, 1:3])
    assert Y3.decompose() == ([0, 1, 2], TO3, Matrix(0, 3, []), Matrix(0, 0, []))
    TO4 = Matrix([[Rational(1, 5), Rational(2, 5), Rational(2, 5)], [Rational(1, 10), S.Half, Rational(2, 5)], [Rational(3, 5), Rational(3, 10), Rational(1, 10)]])
    Y4 = DiscreteMarkovChain('Y', trans_probs=TO4)
    w = ImmutableMatrix([[Rational(11, 39), Rational(16, 39), Rational(4, 13)]])
    assert Y4.limiting_distribution == w
    assert Y4.is_regular() == True
    assert Y4.is_ergodic() == True
    TS1 = MatrixSymbol('T', 3, 3)
    Y5 = DiscreteMarkovChain('Y', trans_probs=TS1)
    assert Y5.limiting_distribution(w, TO4).doit() == True
    assert Y5.stationary_distribution(condition_set=True).subs(TS1, TO4).contains(w).doit() == S.true
    TO6 = Matrix([[S.One, 0, 0, 0, 0],[S.Half, 0, S.Half, 0, 0],[0, S.Half, 0, S.Half, 0], [0, 0, S.Half, 0, S.Half], [0, 0, 0, 0, 1]])
    Y6 = DiscreteMarkovChain('Y', trans_probs=TO6)
    assert Y6.fundamental_matrix() == ImmutableMatrix([[Rational(3, 2), S.One, S.Half], [S.One, S(2), S.One], [S.Half, S.One, Rational(3, 2)]])
    assert Y6.absorbing_probabilities() == ImmutableMatrix([[Rational(3, 4), Rational(1, 4)], [S.Half, S.Half], [Rational(1, 4), Rational(3, 4)]])
    with warns_deprecated_sympy():
        Y6.absorbing_probabilites()
    TO7 = Matrix([[Rational(1, 2), Rational(1, 4), Rational(1, 4)], [Rational(1, 2), 0, Rational(1, 2)], [Rational(1, 4), Rational(1, 4), Rational(1, 2)]])
    Y7 = DiscreteMarkovChain('Y', trans_probs=TO7)
    assert Y7.is_absorbing_chain() == False
    assert Y7.fundamental_matrix() == ImmutableMatrix([[Rational(86, 75), Rational(1, 25), Rational(-14, 75)],
                                                            [Rational(2, 25), Rational(21, 25), Rational(2, 25)],
                                                            [Rational(-14, 75), Rational(1, 25), Rational(86, 75)]])

    # test for zero-sized matrix functionality
    X = DiscreteMarkovChain('X', trans_probs=Matrix([]))
    assert X.number_of_states == 0
    assert X.stationary_distribution() == Matrix([[]])
    assert X.communication_classes() == []
    assert X.canonical_form() == ([], Matrix([]))
    assert X.decompose() == ([], Matrix([]), Matrix([]), Matrix([]))
    assert X.is_regular() == False
    assert X.is_ergodic() == False

    # test communication_class
    # see https://drive.google.com/drive/folders/1HbxLlwwn2b3U8Lj7eb_ASIUb5vYaNIjg?usp=sharing
    # tutorial 2.pdf
    TO7 = Matrix([[0, 5, 5, 0, 0],
                  [0, 0, 0, 10, 0],
                  [5, 0, 5, 0, 0],
                  [0, 10, 0, 0, 0],
                  [0, 3, 0, 3, 4]])/10
    Y7 = DiscreteMarkovChain('Y', trans_probs=TO7)
    tuples = Y7.communication_classes()
    classes, recurrence, periods = list(zip(*tuples))
    assert classes == ([1, 3], [0, 2], [4])
    assert recurrence == (True, False, False)
    assert periods == (2, 1, 1)

    TO8 = Matrix([[0, 0, 0, 10, 0, 0],
                  [5, 0, 5, 0, 0, 0],
                  [0, 4, 0, 0, 0, 6],
                  [10, 0, 0, 0, 0, 0],
                  [0, 10, 0, 0, 0, 0],
                  [0, 0, 0, 5, 5, 0]])/10
    Y8 = DiscreteMarkovChain('Y', trans_probs=TO8)
    tuples = Y8.communication_classes()
    classes, recurrence, periods = list(zip(*tuples))
    assert classes == ([0, 3], [1, 2, 5, 4])
    assert recurrence == (True, False)
    assert periods == (2, 2)

    TO9 = Matrix([[2, 0, 0, 3, 0, 0, 3, 2, 0, 0],
                  [0, 10, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 2, 2, 0, 0, 0, 0, 0, 3, 3],
                  [0, 0, 0, 3, 0, 0, 6, 1, 0, 0],
                  [0, 0, 0, 0, 5, 5, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 10, 0, 0, 0, 0],
                  [4, 0, 0, 5, 0, 0, 1, 0, 0, 0],
                  [2, 0, 0, 4, 0, 0, 2, 2, 0, 0],
                  [3, 0, 1, 0, 0, 0, 0, 0, 4, 2],
                  [0, 0, 4, 0, 0, 0, 0, 0, 3, 3]])/10
    Y9 = DiscreteMarkovChain('Y', trans_probs=TO9)
    tuples = Y9.communication_classes()
    classes, recurrence, periods = list(zip(*tuples))
    assert classes == ([0, 3, 6, 7], [1], [2, 8, 9], [5], [4])
    assert recurrence == (True, True, False, True, False)
    assert periods == (1, 1, 1, 1, 1)

    # test canonical form
    # see https://web.archive.org/web/20201230182007/https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter11.pdf
    # example 11.13
    T = Matrix([[1, 0, 0, 0, 0],
                [S(1) / 2, 0, S(1) / 2, 0, 0],
                [0, S(1) / 2, 0, S(1) / 2, 0],
                [0, 0, S(1) / 2, 0, S(1) / 2],
                [0, 0, 0, 0, S(1)]])
    DW = DiscreteMarkovChain('DW', [0, 1, 2, 3, 4], T)
    states, A, B, C = DW.decompose()
    assert states == [0, 4, 1, 2, 3]
    assert A == Matrix([[1, 0], [0, 1]])
    assert B == Matrix([[S(1)/2, 0], [0, 0], [0, S(1)/2]])
    assert C == Matrix([[0, S(1)/2, 0], [S(1)/2, 0, S(1)/2], [0, S(1)/2, 0]])
    states, new_matrix = DW.canonical_form()
    assert states == [0, 4, 1, 2, 3]
    assert new_matrix == Matrix([[1, 0, 0, 0, 0],
                                 [0, 1, 0, 0, 0],
                                 [S(1)/2, 0, 0, S(1)/2, 0],
                                 [0, 0, S(1)/2, 0, S(1)/2],
                                 [0, S(1)/2, 0, S(1)/2, 0]])

    # test regular and ergodic
    # https://web.archive.org/web/20201230182007/https://www.dartmouth.edu/~chance/teaching_aids/books_articles/probability_book/Chapter11.pdf
    T = Matrix([[0, 4, 0, 0, 0],
                [1, 0, 3, 0, 0],
                [0, 2, 0, 2, 0],
                [0, 0, 3, 0, 1],
                [0, 0, 0, 4, 0]])/4
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert not X.is_regular()
    assert X.is_ergodic()
    T = Matrix([[0, 1], [1, 0]])
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert not X.is_regular()
    assert X.is_ergodic()
    # http://www.math.wisc.edu/~valko/courses/331/MC2.pdf
    T = Matrix([[2, 1, 1],
                [2, 0, 2],
                [1, 1, 2]])/4
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert X.is_regular()
    assert X.is_ergodic()
    # https://docs.ufpr.br/~lucambio/CE222/1S2014/Kemeny-Snell1976.pdf
    T = Matrix([[1, 1], [1, 1]])/2
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert X.is_regular()
    assert X.is_ergodic()

    # test is_absorbing_chain
    T = Matrix([[0, 1, 0],
                [1, 0, 0],
                [0, 0, 1]])
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert not X.is_absorbing_chain()
    # https://en.wikipedia.org/wiki/Absorbing_Markov_chain
    T = Matrix([[1, 1, 0, 0],
                [0, 1, 1, 0],
                [1, 0, 0, 1],
                [0, 0, 0, 2]])/2
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert X.is_absorbing_chain()
    T = Matrix([[2, 0, 0, 0, 0],
                [1, 0, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 1],
                [0, 0, 0, 0, 2]])/2
    X = DiscreteMarkovChain('X', trans_probs=T)
    assert X.is_absorbing_chain()

    # test custom state space
    Y10 = DiscreteMarkovChain('Y', [1, 2, 3], TO2)
    tuples = Y10.communication_classes()
    classes, recurrence, periods = list(zip(*tuples))
    assert classes == ([1], [2, 3])
    assert recurrence == (True, False)
    assert periods == (1, 1)
    assert Y10.canonical_form() == ([1, 2, 3], TO2)
    assert Y10.decompose() == ([1, 2, 3], TO2[0:1, 0:1], TO2[1:3, 0:1], TO2[1:3, 1:3])

    # testing miscellaneous queries
    T = Matrix([[S.Half, Rational(1, 4), Rational(1, 4)],
                [Rational(1, 3), 0, Rational(2, 3)],
                [S.Half, S.Half, 0]])
    X = DiscreteMarkovChain('X', [0, 1, 2], T)
    assert P(Eq(X[1], 2) & Eq(X[2], 1) & Eq(X[3], 0),
    Eq(P(Eq(X[1], 0)), Rational(1, 4)) & Eq(P(Eq(X[1], 1)), Rational(1, 4))) == Rational(1, 12)
    assert P(Eq(X[2], 1) | Eq(X[2], 2), Eq(X[1], 1)) == Rational(2, 3)
    assert P(Eq(X[2], 1) & Eq(X[2], 2), Eq(X[1], 1)) is S.Zero
    assert P(Ne(X[2], 2), Eq(X[1], 1)) == Rational(1, 3)
    assert E(X[1]**2, Eq(X[0], 1)) == Rational(8, 3)
    assert variance(X[1], Eq(X[0], 1)) == Rational(8, 9)
    raises(ValueError, lambda: E(X[1], Eq(X[2], 1)))
    raises(ValueError, lambda: DiscreteMarkovChain('X', [0, 1], T))

    # testing miscellaneous queries with different state space
    X = DiscreteMarkovChain('X', ['A', 'B', 'C'], T)
    assert P(Eq(X[1], 2) & Eq(X[2], 1) & Eq(X[3], 0),
    Eq(P(Eq(X[1], 0)), Rational(1, 4)) & Eq(P(Eq(X[1], 1)), Rational(1, 4))) == Rational(1, 12)
    assert P(Eq(X[2], 1) | Eq(X[2], 2), Eq(X[1], 1)) == Rational(2, 3)
    assert P(Eq(X[2], 1) & Eq(X[2], 2), Eq(X[1], 1)) is S.Zero
    assert P(Ne(X[2], 2), Eq(X[1], 1)) == Rational(1, 3)
    a = X.state_space.args[0]
    c = X.state_space.args[2]
    assert (E(X[1] ** 2, Eq(X[0], 1)) - (a**2/3 + 2*c**2/3)).simplify() == 0
    assert (variance(X[1], Eq(X[0], 1)) - (2*(-a/3 + c/3)**2/3 + (2*a/3 - 2*c/3)**2/3)).simplify() == 0
    raises(ValueError, lambda: E(X[1], Eq(X[2], 1)))

    #testing queries with multiple RandomIndexedSymbols
    T = Matrix([[Rational(5, 10), Rational(3, 10), Rational(2, 10)], [Rational(2, 10), Rational(7, 10), Rational(1, 10)], [Rational(3, 10), Rational(3, 10), Rational(4, 10)]])
    Y = DiscreteMarkovChain("Y", [0, 1, 2], T)
    assert P(Eq(Y[7], Y[5]), Eq(Y[2], 0)).round(5) == Float(0.44428, 5)
    assert P(Gt(Y[3], Y[1]), Eq(Y[0], 0)).round(2) == Float(0.36, 2)
    assert P(Le(Y[5], Y[10]), Eq(Y[4], 2)).round(6) == Float(0.583120, 6)
    assert Float(P(Eq(Y[10], Y[5]), Eq(Y[4], 1)), 14) == Float(1 - P(Ne(Y[10], Y[5]), Eq(Y[4], 1)), 14)
    assert Float(P(Gt(Y[8], Y[9]), Eq(Y[3], 2)), 14) == Float(1 - P(Le(Y[8], Y[9]), Eq(Y[3], 2)), 14)
    assert Float(P(Lt(Y[1], Y[4]), Eq(Y[0], 0)), 14) == Float(1 - P(Ge(Y[1], Y[4]), Eq(Y[0], 0)), 14)
    assert P(Eq(Y[5], Y[10]), Eq(Y[2], 1)) == P(Eq(Y[10], Y[5]), Eq(Y[2], 1))
    assert P(Gt(Y[1], Y[2]), Eq(Y[0], 1)) == P(Lt(Y[2], Y[1]), Eq(Y[0], 1))
    assert P(Ge(Y[7], Y[6]), Eq(Y[4], 1)) == P(Le(Y[6], Y[7]), Eq(Y[4], 1))

    #test symbolic queries
    a, b, c, d = symbols('a b c d')
    T = Matrix([[Rational(1, 10), Rational(4, 10), Rational(5, 10)], [Rational(3, 10), Rational(4, 10), Rational(3, 10)], [Rational(7, 10), Rational(2, 10), Rational(1, 10)]])
    Y = DiscreteMarkovChain("Y", [0, 1, 2], T)
    query = P(Eq(Y[a], b), Eq(Y[c], d))
    assert query.subs({a:10, b:2, c:5, d:1}).evalf().round(4) == P(Eq(Y[10], 2), Eq(Y[5], 1)).round(4)
    assert query.subs({a:15, b:0, c:10, d:1}).evalf().round(4) == P(Eq(Y[15], 0), Eq(Y[10], 1)).round(4)
    query_gt = P(Gt(Y[a], b), Eq(Y[c], d))
    query_le = P(Le(Y[a], b), Eq(Y[c], d))
    assert query_gt.subs({a:5, b:2, c:1, d:0}).evalf() + query_le.subs({a:5, b:2, c:1, d:0}).evalf() == 1.0
    query_ge = P(Ge(Y[a], b), Eq(Y[c], d))
    query_lt = P(Lt(Y[a], b), Eq(Y[c], d))
    assert query_ge.subs({a:4, b:1, c:0, d:2}).evalf() + query_lt.subs({a:4, b:1, c:0, d:2}).evalf() == 1.0

    #test issue 20078
    assert (2*Y[1] + 3*Y[1]).simplify() == 5*Y[1]
    assert (2*Y[1] - 3*Y[1]).simplify() == -Y[1]
    assert (2*(0.25*Y[1])).simplify() == 0.5*Y[1]
    assert ((2*Y[1]) * (0.25*Y[1])).simplify() == 0.5*Y[1]**2
    assert (Y[1]**2 + Y[1]**3).simplify() == (Y[1] + 1)*Y[1]**2

