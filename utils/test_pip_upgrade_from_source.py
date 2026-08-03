import subprocess

def test_pip_upgrade_from_source(
    pip_version, venv_without_setuptools, setuptools_wheel, setuptools_sdist
):
    """
    Check pip can upgrade setuptools from source.
    """
    # Install pip/wheel, in a venv without setuptools (as it
    # should not be needed for bootstrapping from source)
    venv = venv_without_setuptools
    venv.run(["pip", "install", "-U", "wheel"])
    if pip_version is not None:
        venv.run(["python", "-m", "pip", "install", "-U", pip_version, "--retries=1"])
    with pytest.raises(subprocess.CalledProcessError):
        # Meta-test to make sure setuptools is not installed
        venv.run(["python", "-c", "import setuptools"])

    # Then install from wheel.
    venv.run(["pip", "install", str(setuptools_wheel)])
    # And finally try to upgrade from source.
    venv.run(["pip", "install", "--no-cache-dir", "--upgrade", str(setuptools_sdist)])

