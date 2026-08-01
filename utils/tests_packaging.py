
def tests_packaging(session: nox.Session) -> None:
    """
    Run the packaging tests.
    """

    session.install("-r", "tests/requirements.txt", "--prefer-binary")
    session.run("pytest", "tests/extra_python_package", *session.posargs)

