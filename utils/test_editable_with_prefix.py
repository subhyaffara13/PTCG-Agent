
def test_editable_with_prefix(tmp_path, sample_project, editable_opts):
    """
    Editable install to a prefix should be discoverable.
    """
    prefix = tmp_path / 'prefix'

    # figure out where pip will likely install the package
    site_packages_all = [
        prefix / Path(path).relative_to(sys.prefix)
        for path in sys.path
        if 'site-packages' in path and path.startswith(sys.prefix)
    ]

    for sp in site_packages_all:
        sp.mkdir(parents=True)

    # install workaround
    _addsitedirs(site_packages_all)

    env = dict(os.environ, PYTHONPATH=os.pathsep.join(map(str, site_packages_all)))
    cmd = [
        sys.executable,
        '-m',
        'pip',
        'install',
        '--editable',
        str(sample_project),
        '--prefix',
        str(prefix),
        '--no-build-isolation',
        *editable_opts,
    ]
    subprocess.check_call(cmd, env=env)

    # now run 'sample' with the prefix on the PYTHONPATH
    bin = 'Scripts' if platform.system() == 'Windows' else 'bin'
    exe = prefix / bin / 'sample'
    subprocess.check_call([exe], env=env)

