from pathlib import Path


def test_contains_path(other_path, inside, inverted_inside):
    path = Path([(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)], closed=True)
    assert path.contains_path(other_path) is inside
    assert other_path.contains_path(path) is inverted_inside

