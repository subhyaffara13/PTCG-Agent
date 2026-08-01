
def test_couple_2_states():
    # j1=1/2, j2=1/2
    assert JzKetCoupled(0, 0, (S.Half, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(0, 0, (S.Half, S.Half)) )))
    assert JzKetCoupled(1, 1, (S.Half, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(1, 1, (S.Half, S.Half)) )))
    assert JzKetCoupled(1, 0, (S.Half, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(1, 0, (S.Half, S.Half)) )))
    assert JzKetCoupled(1, -1, (S.Half, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(1, -1, (S.Half, S.Half)) )))
    # j1=1, j2=1/2
    assert JzKetCoupled(S.Half, S.Half, (1, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(S.Half, S.Half, (1, S.Half)) )))
    assert JzKetCoupled(S.Half, Rational(-1, 2), (1, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(S.Half, Rational(-1, 2), (1, S.Half)) )))
    assert JzKetCoupled(Rational(3, 2), Rational(3, 2), (1, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), Rational(3, 2), (1, S.Half)) )))
    assert JzKetCoupled(Rational(3, 2), S.Half, (1, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), S.Half, (1, S.Half)) )))
    assert JzKetCoupled(Rational(3, 2), Rational(-1, 2), (1, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), Rational(-1, 2), (1, S.Half)) )))
    assert JzKetCoupled(Rational(3, 2), Rational(-3, 2), (1, S.Half)) == \
        expand(couple(uncouple( JzKetCoupled(Rational(3, 2), Rational(-3, 2), (1, S.Half)) )))
    # j1=1, j2=1
    assert JzKetCoupled(0, 0, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(0, 0, (1, 1)) )))
    assert JzKetCoupled(1, 1, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(1, 1, (1, 1)) )))
    assert JzKetCoupled(1, 0, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(1, 0, (1, 1)) )))
    assert JzKetCoupled(1, -1, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(1, -1, (1, 1)) )))
    assert JzKetCoupled(2, 2, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(2, 2, (1, 1)) )))
    assert JzKetCoupled(2, 1, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(2, 1, (1, 1)) )))
    assert JzKetCoupled(2, 0, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(2, 0, (1, 1)) )))
    assert JzKetCoupled(2, -1, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(2, -1, (1, 1)) )))
    assert JzKetCoupled(2, -2, (1, 1)) == \
        expand(couple(uncouple( JzKetCoupled(2, -2, (1, 1)) )))
    # j1=1/2, j2=3/2
    assert JzKetCoupled(1, 1, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(1, 1, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(1, 0, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(1, 0, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(1, -1, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(1, -1, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(2, 2, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(2, 2, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(2, 1, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(2, 1, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(2, 0, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(2, 0, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(2, -1, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(2, -1, (S.Half, Rational(3, 2))) )))
    assert JzKetCoupled(2, -2, (S.Half, Rational(3, 2))) == \
        expand(couple(uncouple( JzKetCoupled(2, -2, (S.Half, Rational(3, 2))) )))

