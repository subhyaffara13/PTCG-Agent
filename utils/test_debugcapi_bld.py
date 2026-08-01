
def test_debugcapi_bld(hello_world_f90, monkeypatch):
    """Ensures that debugging wrappers work

    CLI :: --debug-capi -c
    """
    ipath = Path(hello_world_f90)
    mname = "blah"
    monkeypatch.setattr(sys, "argv",
                        f'f2py -m {mname} {ipath} -c --debug-capi'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        cmd_run = shlex.split(f"{sys.executable} -c \"import blah; blah.hi()\"")
        rout = subprocess.run(cmd_run, capture_output=True, encoding='UTF-8')
        eout = ' Hello World\n'
        eerr = textwrap.dedent("""\
debug-capi:Python C/API function blah.hi()
debug-capi:float hi=:output,hidden,scalar
debug-capi:hi=0
debug-capi:Fortran subroutine `f2pywraphi(&hi)'
debug-capi:hi=0
debug-capi:Building return value.
debug-capi:Python C/API function blah.hi: successful.
debug-capi:Freeing memory.
        """)
        assert rout.stdout == eout
        assert rout.stderr == eerr

