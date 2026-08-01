
def test__divisor_sigma():
    assert _divisor_sigma(23450) == 50592
    assert _divisor_sigma(23450, 0) == 24
    assert _divisor_sigma(23450, 1) == 50592
    assert _divisor_sigma(23450, 2) == 730747500
    assert _divisor_sigma(23450, 3) == 14666785333344
    A000005 = [1, 2, 2, 3, 2, 4, 2, 4, 3, 4, 2, 6, 2, 4, 4, 5, 2, 6, 2, 6, 4,
               4, 2, 8, 3, 4, 4, 6, 2, 8, 2, 6, 4, 4, 4, 9, 2, 4, 4, 8, 2, 8]
    for n, val in enumerate(A000005, 1):
        assert _divisor_sigma(n, 0) == val
    A000203 = [1, 3, 4, 7, 6, 12, 8, 15, 13, 18, 12, 28, 14, 24, 24, 31, 18,
               39, 20, 42, 32, 36, 24, 60, 31, 42, 40, 56, 30, 72, 32, 63, 48]
    for n, val in enumerate(A000203, 1):
        assert _divisor_sigma(n, 1) == val
    A001157 = [1, 5, 10, 21, 26, 50, 50, 85, 91, 130, 122, 210, 170, 250, 260,
               341, 290, 455, 362, 546, 500, 610, 530, 850, 651, 850, 820, 1050]
    for n, val in enumerate(A001157, 1):
        assert _divisor_sigma(n, 2) == val

