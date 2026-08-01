
def fake_env(
    tmpdir, setup_cfg, setup_py=None, encoding='ascii', package_path='fake_package'
):
    if setup_py is None:
        setup_py = 'from setuptools import setup\nsetup()\n'

    tmpdir.join('setup.py').write(setup_py)
    config = tmpdir.join('setup.cfg')
    config.write(setup_cfg.encode(encoding), mode='wb')

    package_dir, init_file = make_package_dir(package_path, tmpdir)

    init_file.write(
        'VERSION = (1, 2, 3)\n'
        '\n'
        'VERSION_MAJOR = 1'
        '\n'
        'def get_version():\n'
        '    return [3, 4, 5, "dev"]\n'
        '\n'
    )

    return package_dir, config

