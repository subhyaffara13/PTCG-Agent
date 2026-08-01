
def tmpdir_cwd(tmpdir):
    with tmpdir.as_cwd() as orig:
        yield orig

