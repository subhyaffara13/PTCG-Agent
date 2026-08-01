
def gh23598_warn(tmpdir_factory):
    """F90 file for testing warnings in gh23598"""
    fdat = util.getpath("tests", "src", "crackfortran", "gh23598Warn.f90").read_text()
    fn = tmpdir_factory.getbasetemp() / "gh23598Warn.f90"
    fn.write_text(fdat, encoding="ascii")
    return fn

