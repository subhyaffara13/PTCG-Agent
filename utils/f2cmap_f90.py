
def f2cmap_f90(tmpdir_factory):
    """Generates a single f90 file for testing"""
    fdat = util.getpath("tests", "src", "f2cmap", "isoFortranEnvMap.f90").read_text()
    f2cmap = util.getpath("tests", "src", "f2cmap", ".f2py_f2cmap").read_text()
    fn = tmpdir_factory.getbasetemp() / "f2cmap.f90"
    fmap = tmpdir_factory.getbasetemp() / "mapfile"
    fn.write_text(fdat, encoding="ascii")
    fmap.write_text(f2cmap, encoding="ascii")
    return fn

