
def test_branch_cuts():
    assert limit(asin(I*x + 2), x, 0) == pi - asin(2)
    assert limit(asin(I*x + 2), x, 0, '-') == asin(2)
    assert limit(asin(I*x - 2), x, 0) == -asin(2)
    assert limit(asin(I*x - 2), x, 0, '-') == -pi + asin(2)
    assert limit(acos(I*x + 2), x, 0) == -acos(2)
    assert limit(acos(I*x + 2), x, 0, '-') == acos(2)
    assert limit(acos(I*x - 2), x, 0) == acos(-2)
    assert limit(acos(I*x - 2), x, 0, '-') == 2*pi - acos(-2)
    assert limit(atan(x + 2*I), x, 0) == I*atanh(2)
    assert limit(atan(x + 2*I), x, 0, '-') == -pi + I*atanh(2)
    assert limit(atan(x - 2*I), x, 0) == pi - I*atanh(2)
    assert limit(atan(x - 2*I), x, 0, '-') == -I*atanh(2)
    assert limit(atan(1/x), x, 0) == pi/2
    assert limit(atan(1/x), x, 0, '-') == -pi/2
    assert limit(atan(x), x, oo) == pi/2
    assert limit(atan(x), x, -oo) == -pi/2
    assert limit(acot(x + S(1)/2*I), x, 0) == pi - I*acoth(S(1)/2)
    assert limit(acot(x + S(1)/2*I), x, 0, '-') == -I*acoth(S(1)/2)
    assert limit(acot(x - S(1)/2*I), x, 0) == I*acoth(S(1)/2)
    assert limit(acot(x - S(1)/2*I), x, 0, '-') == -pi + I*acoth(S(1)/2)
    assert limit(acot(x), x, 0) == pi/2
    assert limit(acot(x), x, 0, '-') == -pi/2
    assert limit(asec(I*x + S(1)/2), x, 0) == asec(S(1)/2)
    assert limit(asec(I*x + S(1)/2), x, 0, '-') == -asec(S(1)/2)
    assert limit(asec(I*x - S(1)/2), x, 0) == 2*pi - asec(-S(1)/2)
    assert limit(asec(I*x - S(1)/2), x, 0, '-') == asec(-S(1)/2)
    assert limit(acsc(I*x + S(1)/2), x, 0) == acsc(S(1)/2)
    assert limit(acsc(I*x + S(1)/2), x, 0, '-') == pi - acsc(S(1)/2)
    assert limit(acsc(I*x - S(1)/2), x, 0) == -pi + acsc(S(1)/2)
    assert limit(acsc(I*x - S(1)/2), x, 0, '-') == -acsc(S(1)/2)

    assert limit(log(I*x - 1), x, 0) == I*pi
    assert limit(log(I*x - 1), x, 0, '-') == -I*pi
    assert limit(log(-I*x - 1), x, 0) == -I*pi
    assert limit(log(-I*x - 1), x, 0, '-') == I*pi

    assert limit(sqrt(I*x - 1), x, 0) == I
    assert limit(sqrt(I*x - 1), x, 0, '-') == -I
    assert limit(sqrt(-I*x - 1), x, 0) == -I
    assert limit(sqrt(-I*x - 1), x, 0, '-') == I

    assert limit(cbrt(I*x - 1), x, 0) == (-1)**(S(1)/3)
    assert limit(cbrt(I*x - 1), x, 0, '-') == -(-1)**(S(2)/3)
    assert limit(cbrt(-I*x - 1), x, 0) == -(-1)**(S(2)/3)
    assert limit(cbrt(-I*x - 1), x, 0, '-') == (-1)**(S(1)/3)

