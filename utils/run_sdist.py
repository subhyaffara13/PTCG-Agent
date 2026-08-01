
def run_sdist(monkeypatch, project):
    """Given a project directory, run the sdist and return its contents"""
    monkeypatch.chdir(project)
    with quiet():
        run_setup("setup.py", ["sdist"])

    archive = next((project / "dist").glob("*.tar.gz"))
    with tarfile.open(str(archive)) as tar:
        return set(tar.getnames())

