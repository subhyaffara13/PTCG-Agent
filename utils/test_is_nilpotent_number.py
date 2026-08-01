
def test_is_nilpotent_number():
    assert is_nilpotent_number(21) == False
    assert is_nilpotent_number(randprime(1, 30)**12) == True
    raises(ValueError, lambda: is_nilpotent_number(-5))

    A056867	= [1, 2, 3, 4, 5, 7, 8, 9, 11, 13, 15, 16, 17, 19,
               23, 25, 27, 29, 31, 32, 33, 35, 37, 41, 43, 45,
               47, 49, 51, 53, 59, 61, 64, 65, 67, 69, 71, 73,
               77, 79, 81, 83, 85, 87, 89, 91, 95, 97, 99]
    for n in range(1, 100):
        assert is_nilpotent_number(n) == (n in A056867)

