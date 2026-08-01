
def hello_world_f77(tmpdir_factory):
    """Generates a single f77 file for testing"""
    fdat = util.getpath("tests", "src", "cli", "hi77.f").read_text()
    fn = tmpdir_factory.getbasetemp() / "hello.f"
    fn.write_text(fdat, encoding="ascii")
    return fn

