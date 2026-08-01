
def setup_context(tmpdir):
    with (tmpdir / 'setup.py').open('w') as f:
        f.write(SETUP_PY)
    with (tmpdir / 'hi.py').open('w') as f:
        f.write('1\n')
    with tmpdir.as_cwd():
        yield tmpdir

