
def test_include_dirs_after_multiple_compile_calls(c_file):
    """
    Calling compile multiple times should not change the include dirs
    (regression test for setuptools issue #3591).
    """
    compiler = base.new_compiler()
    python = sysconfig.get_paths()['include']
    compiler.set_include_dirs([python])
    compiler.compile([c_file])
    assert compiler.include_dirs == [python]
    compiler.compile([c_file])
    assert compiler.include_dirs == [python]

