
def assert_unordered_tuple_list_equal(a, b, tpl=tuple):
    if isinstance(a, np.ndarray):
        a = a.tolist()
    if isinstance(b, np.ndarray):
        b = b.tolist()
    a = list(map(tpl, a))
    a.sort()
    b = list(map(tpl, b))
    b.sort()
    assert_equal(a, b)

