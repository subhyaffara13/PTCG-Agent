
def test_install_sdist(package, version, tmp_path, venv_python, setuptools_wheel):
    venv_pip = (venv_python, "-m", "pip")
    sdist = retrieve_sdist(package, version, tmp_path)
    deps = build_deps(package, sdist)
    if deps:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Dependencies:", deps)
        run([*venv_pip, "install", *deps])

    # Use a virtualenv to simulate PEP 517 isolation
    # but install fresh setuptools wheel to ensure the version under development
    env = EXTRA_ENV_VARS.get(package, {})
    run([*venv_pip, "install", "--force-reinstall", setuptools_wheel])
    run([*venv_pip, "install", *INSTALL_OPTIONS, sdist], env)

    # Execute a simple script to make sure the package was installed correctly
    pkg = IMPORT_NAME.get(package, package).replace("-", "_")
    script = f"import {pkg}; print(getattr({pkg}, '__version__', 0))"
    run([venv_python, "-c", script])

