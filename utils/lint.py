
def lint(session: nox.Session) -> None:
    """
    Lint the codebase (except for clang-format/tidy).
    """
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a", *session.posargs)

