
def test_K6():
    assert sqrt(x*y*abs(z)**2)/(sqrt(x)*abs(z)) == sqrt(x*y)/sqrt(x)
    assert sqrt(x*y*abs(z)**2)/(sqrt(x)*abs(z)) != sqrt(y)

