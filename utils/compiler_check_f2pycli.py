
def compiler_check_f2pycli():
    if not util.has_fortran_compiler():
        pytest.skip("CLI command needs a Fortran compiler")
    else:
        f2pycli()

