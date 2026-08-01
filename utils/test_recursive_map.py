
def test_recursive_map():
    recursive_map = m.RecursiveMap()
    recursive_map[100] = m.RecursiveMap()
    recursive_map[100][101] = m.RecursiveMap()
    recursive_map[100][102] = m.RecursiveMap()
    assert list(recursive_map[100].keys()) == [101, 102]

