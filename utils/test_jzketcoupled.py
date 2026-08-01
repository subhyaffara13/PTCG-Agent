
def test_jzketcoupled():
    j, m = symbols('j m')
    # j not integer or half integer
    raises(ValueError, lambda: JzKetCoupled(Rational(2, 3), Rational(-1, 3), (1,)))
    raises(ValueError, lambda: JzKetCoupled(Rational(2, 3), m, (1,)))
    # j < 0
    raises(ValueError, lambda: JzKetCoupled(-1, 1, (1,)))
    raises(ValueError, lambda: JzKetCoupled(-1, m, (1,)))
    # m not integer or half integer
    raises(ValueError, lambda: JzKetCoupled(j, Rational(-1, 3), (1,)))
    # abs(m) > j
    raises(ValueError, lambda: JzKetCoupled(1, 2, (1,)))
    raises(ValueError, lambda: JzKetCoupled(1, -2, (1,)))
    # j-m not integer
    raises(ValueError, lambda: JzKetCoupled(1, S.Half, (1,)))
    # checks types on coupling scheme
    raises(TypeError, lambda: JzKetCoupled(1, 1, 1))
    raises(TypeError, lambda: JzKetCoupled(1, 1, (1,), 1))
    raises(TypeError, lambda: JzKetCoupled(1, 1, (1, 1), (1,)))
    raises(TypeError, lambda: JzKetCoupled(1, 1, (1, 1, 1), (1, 2, 1),
           (1, 3, 1)))
    # checks length of coupling terms
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1,), ((1, 2, 1),)))
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((1, 2),)))
    # all jn are integer or half-integer
    raises(ValueError, lambda: JzKetCoupled(1, 1, (Rational(1, 3), Rational(2, 3))))
    # indices in coupling scheme must be integers
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((S.Half, 1, 2),) ))
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((1, S.Half, 2),) ))
    # indices out of range
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((0, 2, 1),) ))
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((3, 2, 1),) ))
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((1, 0, 1),) ))
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((1, 3, 1),) ))
    # all j values in coupling scheme must by integer or half-integer
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1, 1), ((1, 2, S(
        4)/3), (1, 3, 1)) ))
    # each coupling must satisfy |j1-j2| <= j3 <= j1+j2
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 5)))
    raises(ValueError, lambda: JzKetCoupled(5, 1, (1, 1)))
    # final j of coupling must be j of the state
    raises(ValueError, lambda: JzKetCoupled(1, 1, (1, 1), ((1, 2, 2),) ))

