
def test_some_non_alphabet_maintains_order() -> None:
    # 'c beta a' should automatically go to -> 'a c beta'
    string = "c" + chr(ord("b") + 848) + "a"
    # but beta will be temporarily replaced with 'b' for which 'cba->abc'
    # so check manual output kicks in:
    x = np.random.rand(2, 3, 4)
    assert np.allclose(contract(string, x), contract("cxa", x))

