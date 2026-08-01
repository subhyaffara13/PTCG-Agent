
def hello_world_f90(tmpdir_factory):
    """Generates a single f90 file for testing"""
    fdat = util.getpath("tests", "src", "cli", "hiworld.f90").read_text()
    fn = tmpdir_factory.getbasetemp() / "hello.f90"
    fn.write_text(fdat, encoding="ascii")
    return fn

