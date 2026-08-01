
def test_wheel_install(params):
    project_name = params.get('name', 'foo')
    version = params.get('version', '1.0')
    install_requires = params.get('install_requires', [])
    extras_require = params.get('extras_require', {})
    requires_txt = params.get('requires_txt', None)
    install_tree = params.get('install_tree')
    file_defs = params.get('file_defs', {})
    setup_kwargs = params.get('setup_kwargs', {})
    with (
        build_wheel(
            name=project_name,
            version=version,
            install_requires=install_requires,
            extras_require=extras_require,
            extra_file_defs=file_defs,
            **setup_kwargs,
        ) as filename,
        tempdir() as install_dir,
    ):
        _check_wheel_install(
            filename, install_dir, install_tree, project_name, version, requires_txt
        )

