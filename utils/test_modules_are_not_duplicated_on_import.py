
def test_modules_are_not_duplicated_on_import(distutils_version, imported_module, venv):
    env = dict(SETUPTOOLS_USE_DISTUTILS=distutils_version)
    script = ENSURE_IMPORTS_ARE_NOT_DUPLICATED.format(imported_module=imported_module)
    cmd = ['python', '-c', script]
    output = venv.run(cmd, env=win_sr(env), **_TEXT_KWARGS).strip()
    assert output == "success"

