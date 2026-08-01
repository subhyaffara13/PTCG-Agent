
def test_set_include_dirs(c_file):
    """
    Extensions should build even if set_include_dirs is invoked.
    In particular, compiler-specific paths should not be overridden.
    """
    compiler = base.new_compiler()
    python = sysconfig.get_paths()['include']
    compiler.set_include_dirs([python])
    compiler.compile([c_file])

    # do it again, setting include dirs after any initialization
    compiler.set_include_dirs([python])
    compiler.compile([c_file])

