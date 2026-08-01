
def test_Program():
    x = Symbol('x', real=True)
    vx = Variable.deduced(x, 42)
    decl = Declaration(vx)
    prnt = Print([x, x+1])
    prog = Program('foo', [decl, prnt])
    if not has_fortran():
        skip("No fortran compiler found.")

    (stdout, stderr), info = compile_run_strings([('main.f90', fcode(prog, standard=90))], clean=True)
    assert '42' in stdout
    assert '43' in stdout
    assert stderr == ''
    assert info['exit_status'] == os.EX_OK

