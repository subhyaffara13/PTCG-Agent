from pathlib import Path


def test_make_compound_path_stops():
    zero = [0, 0]
    paths = 3*[Path([zero, zero], [Path.MOVETO, Path.STOP])]
    compound_path = Path.make_compound_path(*paths)
    # the choice to not preserve the terminal STOP is arbitrary, but
    # documented, so we test that it is in fact respected here
    assert np.sum(compound_path.codes == Path.STOP) == 0

