
def sample_project_cwd(sample_project):
    with path.Path(sample_project):
        yield

