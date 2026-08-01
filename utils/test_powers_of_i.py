
def test_powers_of_I():
    assert [sqrt(I)**i for i in range(13)] == [
        1, sqrt(I), I, sqrt(I)**3, -1, -sqrt(I), -I, -sqrt(I)**3,
        1, sqrt(I), I, sqrt(I)**3, -1]
    assert sqrt(I)**(S(9)/2) == -I**(S(1)/4)

