
def gh22819_cli(tmpdir_factory):
    """F90 file for testing disallowed CLI arguments in ghff819"""
    fdat = util.getpath("tests", "src", "cli", "gh_22819.pyf").read_text()
    fn = tmpdir_factory.getbasetemp() / "gh_22819.pyf"
    fn.write_text(fdat, encoding="ascii")
    return fn

