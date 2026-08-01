
def build_wheel(extra_file_defs=None, **kwargs):
    file_defs = {
        'setup.py': (
            DALS(
                """
            # -*- coding: utf-8 -*-
            from setuptools import setup
            import setuptools
            setup(**%r)
            """
            )
            % kwargs
        ).encode('utf-8'),
    }
    if extra_file_defs:
        file_defs.update(extra_file_defs)
    with tempdir() as source_dir:
        path.build(file_defs, source_dir)
        subprocess.check_call(
            (sys.executable, 'setup.py', '-q', 'bdist_wheel'), cwd=source_dir
        )
        yield glob.glob(os.path.join(source_dir, 'dist', '*.whl'))[0]


def build_wheel(wheel_directory, config_settings, metadata_directory=None):
    """Invoke the mandatory build_wheel hook.

    If a wheel was already built in the
    prepare_metadata_for_build_wheel fallback, this
    will copy it rather than rebuilding the wheel.
    """
    prebuilt_whl = _find_already_built_wheel(metadata_directory)
    if prebuilt_whl:
        shutil.copy2(prebuilt_whl, wheel_directory)
        return os.path.basename(prebuilt_whl)

    return _build_backend().build_wheel(
        wheel_directory, config_settings, metadata_directory
    )

