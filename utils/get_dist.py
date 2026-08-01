
def get_dist(tmpdir, kwargs_initial=None, parse=True):
    kwargs_initial = kwargs_initial or {}

    with tmpdir.as_cwd():
        dist = Distribution(kwargs_initial)
        dist.script_name = 'setup.py'
        parse and dist.parse_config_files()

        yield dist

