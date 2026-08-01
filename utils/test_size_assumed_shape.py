
def test_size_assumed_shape():
    if not has_fortran():
        skip("No fortran compiler found.")
    a = Symbol('a', real=True)
    body = [Return((sum_(a**2)/size(a))**.5)]
    arr = array(a, dim=[':'], intent='in')
    fd = FunctionDefinition(real, 'rms', [arr], body)
    render_as_module([fd], 'mod_rms')

    (stdout, stderr), info = compile_run_strings([
        ('rms.f90', render_as_module([fd], 'mod_rms')),
        ('main.f90', (
            'program myprog\n'
            'use mod_rms, only: rms\n'
            'real*8, dimension(4), parameter :: x = [4, 2, 2, 2]\n'
            'print "(f7.5)", dsqrt(7d0) - rms(x)\n'
            'end program\n'
        ))
    ], clean=True)
    assert '0.00000' in stdout
    assert stderr == ''
    assert info['exit_status'] == os.EX_OK

