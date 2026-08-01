
def project_dir(request, distutils_managed_tempdir):
    self = request.instance
    self.tmp_dir = self.mkdtemp()
    jaraco.path.build(
        {
            'somecode': {
                '__init__.py': '#',
            },
            'README': 'xxx',
            'setup.py': SETUP_PY,
        },
        self.tmp_dir,
    )
    with path.Path(self.tmp_dir):
        yield

