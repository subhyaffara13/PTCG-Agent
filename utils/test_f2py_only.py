
def test_f2py_only(capfd, retreal_f77, monkeypatch):
    """Test that functions can be kept by only:
    CLI :: only:
    """
    foutl = get_io_paths(retreal_f77, mname="test")
    ipath = foutl.finp
    toskip = "t0 t4 t8 sd s8 s4"
    tokeep = "td s0"
    monkeypatch.setattr(
        sys, "argv",
        f'f2py {ipath} -m test only: {tokeep}'.split())

    with util.switchdir(ipath.parent):
        f2pycli()
        out, err = capfd.readouterr()
        for skey in toskip.split():
            assert (
                f'buildmodule: Could not find the body of interfaced routine "{skey}". Skipping.'
                in err)
        for rkey in tokeep.split():
            assert f'Constructing wrapper function "{rkey}"' in out

