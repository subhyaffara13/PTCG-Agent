
def write_requirements(cmd, basename, filename):
    dist = cmd.distribution
    data = io.StringIO()
    install_requires, extras_require = _prepare(
        dist.install_requires or (), dist.extras_require or {}
    )
    _write_requirements(data, install_requires)
    for extra in sorted(extras_require):
        data.write('\n[{extra}]\n'.format(**vars()))
        _write_requirements(data, extras_require[extra])
    cmd.write_or_delete_file("requirements", filename, data.getvalue())

