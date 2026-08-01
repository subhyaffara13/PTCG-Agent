
def test_pep338():
    stdout = subprocess.check_output([sys.executable, '-mnumpy.f2py', '-v'])
    assert_equal(stdout.strip(), np.__version__.encode('ascii'))

