
def test_log_module_is_not_duplicated_on_import(distutils_version, venv):
    env = dict(SETUPTOOLS_USE_DISTUTILS=distutils_version)
    cmd = ['python', '-c', ENSURE_LOG_IMPORT_IS_NOT_DUPLICATED]
    output = venv.run(cmd, env=win_sr(env), **_TEXT_KWARGS).strip()
    assert output == "success"

