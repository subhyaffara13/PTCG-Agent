
def test_comp1():
    # sqrt(2) = 1.414213 5623730950...
    a = sqrt(2).n(7)
    assert comp(a, 1.4142129) is False
    assert comp(a, 1.4142130)
    #                  ...
    assert comp(a, 1.4142141)
    assert comp(a, 1.4142142) is False
    assert comp(sqrt(2).n(2), '1.4')
    assert comp(sqrt(2).n(2), Float(1.4, 2), '')
    assert comp(sqrt(2).n(2), 1.4, '')
    assert comp(sqrt(2).n(2), Float(1.4, 3), '') is False
    assert comp(sqrt(2) + sqrt(3)*I, 1.4 + 1.7*I, .1)
    assert not comp(sqrt(2) + sqrt(3)*I, (1.5 + 1.7*I)*0.89, .1)
    assert comp(sqrt(2) + sqrt(3)*I, (1.5 + 1.7*I)*0.90, .1)
    assert comp(sqrt(2) + sqrt(3)*I, (1.5 + 1.7*I)*1.07, .1)
    assert not comp(sqrt(2) + sqrt(3)*I, (1.5 + 1.7*I)*1.08, .1)
    assert [(i, j)
            for i in range(130, 150)
            for j in range(170, 180)
            if comp((sqrt(2)+ I*sqrt(3)).n(3), i/100. + I*j/100.)] == [
        (141, 173), (142, 173)]
    raises(ValueError, lambda: comp(t, '1'))
    raises(ValueError, lambda: comp(t, 1))
    assert comp(0, 0.0)
    assert comp(.5, S.Half)
    assert comp(2 + sqrt(2), 2.0 + sqrt(2))
    assert not comp(0, 1)
    assert not comp(2, sqrt(2))
    assert not comp(2 + I, 2.0 + sqrt(2))
    assert not comp(2.0 + sqrt(2), 2 + I)
    assert not comp(2.0 + sqrt(2), sqrt(3))
    assert comp(1/pi.n(4), 0.3183, 1e-5)
    assert not comp(1/pi.n(4), 0.3183, 8e-6)

