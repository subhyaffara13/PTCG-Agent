
def baseline_setup():
    """Baseline setup by creating temp folder and resetting repo."""
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d, True)

    if repo:
        repo.head.reset(commit=current_commit, working_tree=True)

