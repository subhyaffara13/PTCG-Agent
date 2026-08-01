
def make_changelog(session: nox.Session) -> None:
    """
    Inspect the closed issues and make entries for a changelog.
    """
    session.install("ghapi", "rich")
    session.run("python", "tools/make_changelog.py")

