
def test_issue_19113_19102():
    t = S(1)/3
    solve(cos(x)**5-sin(x)**5)
    assert solve(4*cos(x)**3 - 2*sin(x)**3) == [
        atan(2**(t)), -atan(2**(t)*(1 - sqrt(3)*I)/2),
        -atan(2**(t)*(1 + sqrt(3)*I)/2)]
    h = S.Half
    assert solve(cos(x)**2 + sin(x)) == [
        2*atan(-h + sqrt(5)/2 + sqrt(2)*sqrt(1 - sqrt(5))/2),
        -2*atan(h + sqrt(5)/2 + sqrt(2)*sqrt(1 + sqrt(5))/2),
        -2*atan(-sqrt(5)/2 + h + sqrt(2)*sqrt(1 - sqrt(5))/2),
        -2*atan(-sqrt(2)*sqrt(1 + sqrt(5))/2 + h + sqrt(5)/2)]
    assert solve(3*cos(x) - sin(x)) == [atan(3)]

