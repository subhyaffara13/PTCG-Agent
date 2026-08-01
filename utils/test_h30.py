
def test_H30():
    test = factor(x**3 + y**3, extension=sqrt(-3))
    answer = (x + y)*(x + y*(-R(1, 2) - sqrt(3)/2*I))*(x + y*(-R(1, 2) + sqrt(3)/2*I))
    assert answer == test

