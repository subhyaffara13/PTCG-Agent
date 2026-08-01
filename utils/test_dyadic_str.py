
def test_dyadic_str():
    assert vsprint(Dyadic([])) == '0'
    assert vsprint(y) == 'a**2*(N.x|N.y) + b*(N.y|N.y) + c*sin(alpha)*(N.z|N.y)'
    assert vsprint(x) == 'alpha*(N.x|N.x) + sin(omega)*(N.y|N.z) + alpha*beta*(N.z|N.x)'
    assert vsprint(ww) == "alpha*N.x + asin(omega)*N.y - beta*alpha'*N.z"
    assert vsprint(xx) == '- (N.x|N.y) - (N.x|N.z)'
    assert vsprint(xx2) == '(N.x|N.y) + (N.x|N.z)'

