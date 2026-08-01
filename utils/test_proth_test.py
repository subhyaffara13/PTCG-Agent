
def test_proth_test():
    # Proth number
    A080075 = [3, 5, 9, 13, 17, 25, 33, 41, 49, 57, 65,
               81, 97, 113, 129, 145, 161, 177, 193]
    # Proth prime
    A080076 = [3, 5, 13, 17, 41, 97, 113, 193]

    for n in range(200):
        if n in A080075:
            assert proth_test(n) == (n in A080076)
        else:
            raises(ValueError, lambda: proth_test(n))

