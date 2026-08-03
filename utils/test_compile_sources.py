import os
import subprocess

def test_compile_sources():
    tmpdir = tempfile.mkdtemp()

    from sympy.utilities._compilation import has_c
    if not has_c():
        skip("No C compiler found.")

    build_dir = str(tmpdir)
    _handle, file_path = tempfile.mkstemp('.c', dir=build_dir)
    with open(file_path, 'wt') as ofh:
        ofh.write("""
        int foo(int bar) {
            return 2*bar;
        }
        """)
    obj, = compile_sources([file_path], cwd=build_dir)
    obj_path = get_abspath(obj, cwd=build_dir)
    assert os.path.exists(obj_path)
    try:
        _ = subprocess.check_output(["nm", "--help"])
    except subprocess.CalledProcessError:
        pass  # we cannot test contents of object file
    else:
        nm_out = subprocess.check_output(["nm", obj_path])
        assert 'foo' in nm_out.decode('utf-8')

    if not cython:
        return  # the final (optional) part of the test below requires Cython.

    _handle, pyx_path = tempfile.mkstemp('.pyx', dir=build_dir)
    with open(pyx_path, 'wt') as ofh:
        ofh.write(("cdef extern int foo(int)\n"
                   "def _foo(arg):\n"
                   "    return foo(arg)"))
    mod = compile_link_import_py_ext([pyx_path], extra_objs=[obj_path], build_dir=build_dir)
    assert mod._foo(21) == 42

