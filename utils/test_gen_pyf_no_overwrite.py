
def test_gen_pyf_no_overwrite(capfd, hello_world_f90, monkeypatch):
    """Ensures that the CLI refuses to overwrite signature files
    CLI :: -h without --overwrite-signature
    """
    ipath = Path(hello_world_f90)
    monkeypatch.setattr(sys, "argv", f'f2py -h faker.pyf {ipath}'.split())

    with util.switchdir(ipath.parent):
        Path("faker.pyf").write_text("Fake news", encoding="ascii")
        with pytest.raises(SystemExit):
            f2pycli()  # Refuse to overwrite
            _, err = capfd.readouterr()
            assert "Use --overwrite-signature to overwrite" in err

