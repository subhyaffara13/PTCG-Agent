
def test_consistent_error_from_modified_py(distutils_version, imported_module, venv):
    env = dict(SETUPTOOLS_USE_DISTUTILS=distutils_version)
    cmd = [
        'python',
        '-c',
        ENSURE_CONSISTENT_ERROR_FROM_MODIFIED_PY.format(
            imported_module=imported_module
        ),
    ]
    output = venv.run(cmd, env=win_sr(env), **_TEXT_KWARGS).strip()
    assert output == "success"

