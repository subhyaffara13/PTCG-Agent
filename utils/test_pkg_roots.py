
def test_pkg_roots(tmp_path):
    """This test focus in getting a particular implementation detail right.
    If at some point in time the implementation is changed for something different,
    this test can be modified or even excluded.
    """
    files = {
        "a": {"b": {"__init__.py": "ab = 1"}, "__init__.py": "a = 1"},
        "d": {"__init__.py": "d = 1", "e": {"__init__.py": "de = 1"}},
        "f": {"g": {"h": {"__init__.py": "fgh = 1"}}},
        "other": {"__init__.py": "abc = 1"},
        "another": {"__init__.py": "abcxyz = 1"},
        "yet_another": {"__init__.py": "mnopq = 1"},
    }
    jaraco.path.build(files, prefix=tmp_path)
    package_dir = {
        "a.b.c": "other",
        "a.b.c.x.y.z": "another",
        "m.n.o.p.q": "yet_another",
    }
    packages = [
        "a",
        "a.b",
        "a.b.c",
        "a.b.c.x.y",
        "a.b.c.x.y.z",
        "d",
        "d.e",
        "f",
        "f.g",
        "f.g.h",
        "m.n.o.p.q",
    ]
    roots = _find_package_roots(packages, package_dir, tmp_path)
    assert roots == {
        "a": str(tmp_path / "a"),
        "a.b.c": str(tmp_path / "other"),
        "a.b.c.x.y.z": str(tmp_path / "another"),
        "d": str(tmp_path / "d"),
        "f": str(tmp_path / "f"),
        "m.n.o.p.q": str(tmp_path / "yet_another"),
    }

    ns = set(dict(_find_namespaces(packages, roots)))
    assert ns == {"f", "f.g"}

    ns = set(_find_virtual_namespaces(roots))
    assert ns == {"a.b", "a.b.c.x", "a.b.c.x.y", "m", "m.n", "m.n.o", "m.n.o.p"}

