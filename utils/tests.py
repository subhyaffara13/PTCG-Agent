
def tests(session: nox.Session) -> None:
    """
    Run the tests (requires a compiler).
    """
    tmpdir = session.create_tmp()
    session.install("cmake")
    session.install("-r", "tests/requirements.txt")
    session.run(
        "cmake",
        "-S.",
        f"-B{tmpdir}",
        "-DPYBIND11_WERROR=ON",
        "-DDOWNLOAD_CATCH=ON",
        "-DDOWNLOAD_EIGEN=ON",
        *session.posargs,
    )
    session.run("cmake", "--build", tmpdir)
    session.run("cmake", "--build", tmpdir, "--config=Release", "--target", "check")


def tests():
    """
    >>> serialized = dill.dumps(lambda x: x)
    """
    return

