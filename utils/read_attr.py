
def read_attr(
    attr_desc: str,
    package_dir: Mapping[str, str] | None = None,
    root_dir: StrPath | None = None,
) -> Any:
    """Reads the value of an attribute from a module.

    This function will try to read the attributed statically first
    (via :func:`ast.literal_eval`), and only evaluate the module if it fails.

    Examples:
        read_attr("package.attr")
        read_attr("package.module.attr")

    :param str attr_desc: Dot-separated string describing how to reach the
        attribute (see examples above)
    :param dict[str, str] package_dir: Mapping of package names to their
        location in disk (represented by paths relative to ``root_dir``).
    :param str root_dir: Path to directory containing all the packages in
        ``package_dir`` (current directory by default).
    :rtype: str
    """
    root_dir = root_dir or os.getcwd()
    attrs_path = attr_desc.strip().split('.')
    attr_name = attrs_path.pop()
    module_name = '.'.join(attrs_path)
    module_name = module_name or '__init__'
    path = _find_module(module_name, package_dir, root_dir)
    spec = _find_spec(module_name, path)

    try:
        value = getattr(StaticModule(module_name, spec), attr_name)
        # XXX: Is marking as static contents coming from modules too optimistic?
        return _static.attempt_conversion(value)
    except Exception:
        # fallback to evaluate module
        module = _load_spec(spec, module_name)
        return getattr(module, attr_name)

