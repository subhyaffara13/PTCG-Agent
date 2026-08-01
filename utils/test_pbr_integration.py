
def test_pbr_integration(pbr_package, venv, editable_opts):
    """Ensure editable installs work with pbr, issue #3500"""
    cmd = [
        'python',
        '-m',
        'pip',
        '-v',
        'install',
        '--editable',
        pbr_package,
        *editable_opts,
    ]
    venv.run(cmd, stderr=subprocess.STDOUT)
    out = venv.run(["python", "-c", "import mypkg.hello"])
    assert "Hello world!" in out


def test_pbr_integration(pbr_package, venv):
    """Ensure pbr packages install."""
    cmd = [
        'python',
        '-m',
        'pip',
        '-v',
        'install',
        '--no-build-isolation',
        pbr_package,
    ]
    venv.run(cmd, stderr=subprocess.STDOUT)
    out = venv.run(["python", "-c", "import mypkg.hello"])
    assert "Hello world!" in out

