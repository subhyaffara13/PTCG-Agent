
def build_namespace_package(tmpdir, name, version="1.0", impl="pkg_resources"):
    src_dir = tmpdir / name
    src_dir.mkdir()
    setup_py = src_dir / 'setup.py'
    namespace, _, rest = name.rpartition('.')
    namespaces = list(iter_namespace_pkgs(namespace))
    setup_args = {
        "name": name,
        "version": version,
        "packages": namespaces,
    }

    if impl == "pkg_resources":
        tmpl = '__import__("pkg_resources").declare_namespace(__name__)'
        setup_args["namespace_packages"] = namespaces
    elif impl == "pkgutil":
        tmpl = '__path__ = __import__("pkgutil").extend_path(__path__, __name__)'
    else:
        raise ValueError(f"Cannot recognise {impl=} when creating namespaces")

    args = json.dumps(setup_args, indent=4)
    assert ast.literal_eval(args)  # ensure it is valid Python

    script = textwrap.dedent(
        """\
        import setuptools
        args = {args}
        setuptools.setup(**args)
        """
    ).format(args=args)
    setup_py.write_text(script, encoding='utf-8')

    ns_pkg_dir = Path(src_dir, namespace.replace(".", "/"))
    ns_pkg_dir.mkdir(parents=True)

    for ns in namespaces:
        pkg_init = src_dir / ns.replace(".", "/") / '__init__.py'
        pkg_init.write_text(tmpl, encoding='utf-8')

    pkg_mod = ns_pkg_dir / (rest + '.py')
    some_functionality = 'name = {rest!r}'.format(**locals())
    pkg_mod.write_text(some_functionality, encoding='utf-8')
    return src_dir

