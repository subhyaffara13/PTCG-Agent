
def test_eval_approx_relative():
    CRootOf.clear_cache()
    t = [CRootOf(x**3 + 10*x + 1, i) for i in range(3)]
    assert [i.eval_rational(1e-1) for i in t] == [
        Rational(-21, 220), Rational(15, 256) - I*805/256,
        Rational(15, 256) + I*805/256]
    t[0]._reset()
    assert [i.eval_rational(1e-1, 1e-4) for i in t] == [
        Rational(-21, 220), Rational(3275, 65536) - I*414645/131072,
        Rational(3275, 65536) + I*414645/131072]
    assert S(t[0]._get_interval().dx) < 1e-1
    assert S(t[1]._get_interval().dx) < 1e-1
    assert S(t[1]._get_interval().dy) < 1e-4
    assert S(t[2]._get_interval().dx) < 1e-1
    assert S(t[2]._get_interval().dy) < 1e-4
    t[0]._reset()
    assert [i.eval_rational(1e-4, 1e-4) for i in t] == [
        Rational(-2001, 20020), Rational(6545, 131072) - I*414645/131072,
        Rational(6545, 131072) + I*414645/131072]
    assert S(t[0]._get_interval().dx) < 1e-4
    assert S(t[1]._get_interval().dx) < 1e-4
    assert S(t[1]._get_interval().dy) < 1e-4
    assert S(t[2]._get_interval().dx) < 1e-4
    assert S(t[2]._get_interval().dy) < 1e-4
    # in the following, the actual relative precision is
    # less than tested, but it should never be greater
    t[0]._reset()
    assert [i.eval_rational(n=2) for i in t] == [
        Rational(-202201, 2024022), Rational(104755, 2097152) - I*6634255/2097152,
        Rational(104755, 2097152) + I*6634255/2097152]
    assert abs(S(t[0]._get_interval().dx)/t[0]) < 1e-2
    assert abs(S(t[1]._get_interval().dx)/t[1]).n() < 1e-2
    assert abs(S(t[1]._get_interval().dy)/t[1]).n() < 1e-2
    assert abs(S(t[2]._get_interval().dx)/t[2]).n() < 1e-2
    assert abs(S(t[2]._get_interval().dy)/t[2]).n() < 1e-2
    t[0]._reset()
    assert [i.eval_rational(n=3) for i in t] == [
        Rational(-202201, 2024022), Rational(1676045, 33554432) - I*106148135/33554432,
        Rational(1676045, 33554432) + I*106148135/33554432]
    assert abs(S(t[0]._get_interval().dx)/t[0]) < 1e-3
    assert abs(S(t[1]._get_interval().dx)/t[1]).n() < 1e-3
    assert abs(S(t[1]._get_interval().dy)/t[1]).n() < 1e-3
    assert abs(S(t[2]._get_interval().dx)/t[2]).n() < 1e-3
    assert abs(S(t[2]._get_interval().dy)/t[2]).n() < 1e-3

    t[0]._reset()
    a = [i.eval_approx(2) for i in t]
    assert [str(i) for i in a] == [
        '-0.10', '0.05 - 3.2*I', '0.05 + 3.2*I']
    assert all(abs(((a[i] - t[i])/t[i]).n()) < 1e-2 for i in range(len(a)))

