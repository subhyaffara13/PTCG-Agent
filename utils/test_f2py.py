import subprocess

def test_f2py(f2py_cmd):
    # test that we can run f2py script
    stdout = subprocess.check_output([f2py_cmd, '-v'])
    assert_equal(stdout.strip(), np.__version__.encode('ascii'))

