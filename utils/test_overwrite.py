import sys
from pathlib import Path


def test_overwrite():
    G = np.array([[0, 3, 3, 1, 2],
                  [3, 0, 0, 2, 4],
                  [3, 0, 0, 0, 0],
                  [1, 2, 0, 0, 2],
                  [2, 4, 0, 2, 0]], dtype=float)
    foo = G.copy()
    shortest_path(foo, overwrite=False)
    assert_array_equal(foo, G)


def test_overwrite(routine, dtype, shape, axis, type, norm, overwrite_x):
    # Check input overwrite behavior
    np.random.seed(1234)
    if np.issubdtype(dtype, np.complexfloating):
        x = np.random.randn(*shape) + 1j*np.random.randn(*shape)
    else:
        x = np.random.randn(*shape)
    x = x.astype(dtype)
    x2 = x.copy()
    routine(x2, type, None, axis, norm, overwrite_x=overwrite_x)

    sig = (f"{routine.__name__}({x.dtype}{x.shape!r}, {None!r}, axis={axis!r}, "
           f"overwrite_x={overwrite_x!r})")
    if not overwrite_x:
        assert_equal(x2, x, err_msg=f"spurious overwrite in {sig}")


def test_overwrite(capfd, hello_world_f90, monkeypatch):
    """Ensures that the build directory can be specified

    CLI :: --overwrite-signature
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(
        sys, "argv",
        f'f2py -h faker.pyf {ipath} --overwrite-signature'.split())

    with util.switchdir(ipath.parent):
        Path("faker.pyf").write_text("Fake news", encoding="ascii")
        f2pycli()
        out, _ = capfd.readouterr()
        assert "Saving signatures to file" in out

