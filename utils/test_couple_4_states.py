
def test_couple_4_states():
    # Default coupling
    # j1=1/2, j2=1/2, j3=1/2, j4=1/2
    assert JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(
            uncouple( JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(
            uncouple( JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(uncouple(
            JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(2, 2, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(
            uncouple( JzKetCoupled(2, 2, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(2, 1, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(
            uncouple( JzKetCoupled(2, 1, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(
            uncouple( JzKetCoupled(2, 0, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(2, -1, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(uncouple(
            JzKetCoupled(2, -1, (S.Half, S.Half, S.Half, S.Half)) )))
    assert JzKetCoupled(2, -2, (S.Half, S.Half, S.Half, S.Half)) == \
        expand(couple(uncouple(
            JzKetCoupled(2, -2, (S.Half, S.Half, S.Half, S.Half)) )))
    # j1=1/2, j2=1/2, j3=1/2, j4=1
    assert JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(5, 2), Rational(5, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(5, 2), Rational(5, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(5, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(5, 2), S.Half, (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(5, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(5, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1)) )))
    assert JzKetCoupled(Rational(5, 2), Rational(-5, 2), (S.Half, S.Half, S.Half, 1)) == \
        expand(couple(uncouple(
            JzKetCoupled(Rational(5, 2), Rational(-5, 2), (S.Half, S.Half, S.Half, 1)) )))
    # Coupling j1+j3=j13, j2+j4=j24, j13+j24=j
    # j1=1/2, j2=1/2, j3=1/2, j4=1/2, j13=1, j24=0
    assert JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 3, 1), (2, 4, 0), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, 1, (S.Half, S.Half, S.Half, S.Half), ((1, 3, 1), (2, 4, 0), (1, 2, 1)) ) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 3, 1), (2, 4, 0), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, 0, (S.Half, S.Half, S.Half, S.Half), ((1, 3, 1), (2, 4, 0), (1, 2, 1)) ) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 3, 1), (2, 4, 0), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, -1, (S.Half, S.Half, S.Half, S.Half), ((1, 3, 1), (2, 4, 0), (1, 2, 1)) ) ), ((1, 3), (2, 4), (1, 2)) ))
    # j1=1/2, j2=1/2, j3=1/2, j4=1, j13=1, j24=1/2
    assert JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, S.Half)) ) == \
        expand(couple(uncouple( JzKetCoupled(S.Half, S.Half, (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, S.Half)) )), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, S.Half)) ) == \
        expand(couple(uncouple( JzKetCoupled(S.Half, Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, S.Half)) ) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), Rational(3, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), S.Half, (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), Rational(-1, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), Rational(-3, 2), (S.Half, S.Half, S.Half, 1), ((1, 3, 1), (2, 4, S.Half), (1, 2, Rational(3, 2))) ) ), ((1, 3), (2, 4), (1, 2)) ))
    # j1=1/2, j2=1, j3=1/2, j4=1, j13=0, j24=1
    assert JzKetCoupled(1, 1, (S.Half, 1, S.Half, 1), ((1, 3, 0), (2, 4, 1), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, 1, (S.Half, 1, S.Half, 1), (
            (1, 3, 0), (2, 4, 1), (1, 2, 1))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, 0, (S.Half, 1, S.Half, 1), ((1, 3, 0), (2, 4, 1), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, 0, (S.Half, 1, S.Half, 1), (
            (1, 3, 0), (2, 4, 1), (1, 2, 1))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, -1, (S.Half, 1, S.Half, 1), ((1, 3, 0), (2, 4, 1), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, -1, (S.Half, 1, S.Half, 1), (
            (1, 3, 0), (2, 4, 1), (1, 2, 1))) ), ((1, 3), (2, 4), (1, 2)) ))
    # j1=1/2, j2=1, j3=1/2, j4=1, j13=1, j24=1
    assert JzKetCoupled(0, 0, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 0)) ) == \
        expand(couple(uncouple( JzKetCoupled(0, 0, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 0))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, 1, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, 1, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 1))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, 0, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, 0, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 1))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(1, -1, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 1)) ) == \
        expand(couple(uncouple( JzKetCoupled(1, -1, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 1))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(2, 2, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 2)) ) == \
        expand(couple(uncouple( JzKetCoupled(2, 2, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 2))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(2, 1, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 2)) ) == \
        expand(couple(uncouple( JzKetCoupled(2, 1, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 2))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(2, 0, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 2)) ) == \
        expand(couple(uncouple( JzKetCoupled(2, 0, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 2))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(2, -1, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 2)) ) == \
        expand(couple(uncouple( JzKetCoupled(2, -1, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 2))) ), ((1, 3), (2, 4), (1, 2)) ))
    assert JzKetCoupled(2, -2, (S.Half, 1, S.Half, 1), ((1, 3, 1), (2, 4, 1), (1, 2, 2)) ) == \
        expand(couple(uncouple( JzKetCoupled(2, -2, (S.Half, 1, S.Half, 1), (
            (1, 3, 1), (2, 4, 1), (1, 2, 2))) ), ((1, 3), (2, 4), (1, 2)) ))

