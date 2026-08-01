
def test_is_abelian_number():
    assert is_abelian_number(4) == True
    assert is_abelian_number(randprime(1, 2000)**2) == True
    assert is_abelian_number(randprime(1000, 100000)) == True
    assert is_abelian_number(60) == False
    assert is_abelian_number(24) == False
    raises(ValueError, lambda: is_abelian_number(-5))

    A051532 = [1, 2, 3, 4, 5, 7, 9, 11, 13, 15, 17, 19, 23, 25,
               29, 31, 33, 35, 37, 41, 43, 45, 47, 49, 51, 53,
               59, 61, 65, 67, 69, 71, 73, 77, 79, 83, 85, 87,
               89, 91, 95, 97, 99]
    for n in range(1, 100):
        assert is_abelian_number(n) == (n in A051532)

