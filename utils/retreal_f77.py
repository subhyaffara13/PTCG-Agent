
def retreal_f77(tmpdir_factory):
    """Generates a single f77 file for testing"""
    fdat = util.getpath("tests", "src", "return_real", "foo77.f").read_text()
    fn = tmpdir_factory.getbasetemp() / "foo.f"
    fn.write_text(fdat, encoding="ascii")
    return fn

