
def user_site_dir(request):
    self = request.instance
    self.tmp_dir = self.mkdtemp()
    self.tmp_path = path.Path(self.tmp_dir)
    from distutils.command import build_ext

    orig_user_base = site.USER_BASE

    site.USER_BASE = self.mkdtemp()
    build_ext.USER_BASE = site.USER_BASE

    # bpo-30132: On Windows, a .pdb file may be created in the current
    # working directory. Create a temporary working directory to cleanup
    # everything at the end of the test.
    with self.tmp_path:
        yield

    site.USER_BASE = orig_user_base
    build_ext.USER_BASE = orig_user_base

    if sys.platform == 'cygwin':
        time.sleep(1)

