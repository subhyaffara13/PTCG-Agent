
def test_all_classes_are_tested():
    this = os.path.split(__file__)[0]
    path = os.path.join(this, os.pardir, os.pardir)
    sympy_path = os.path.abspath(path)
    prefix = os.path.split(sympy_path)[0] + os.sep

    re_cls = re.compile(r"^class ([A-Za-z][A-Za-z0-9_]*)\s*\(", re.MULTILINE)

    modules = {}

    for root, dirs, files in os.walk(sympy_path):
        module = root.replace(prefix, "").replace(os.sep, ".")

        for file in files:
            if file.startswith(("_", "test_", "bench_")):
                continue
            if not file.endswith(".py"):
                continue

            text = Path(os.path.join(root, file)).read_text(encoding='utf-8')

            submodule = module + '.' + file[:-3]

            if any(submodule.startswith(wpath) for wpath in whitelist):
                continue

            names = re_cls.findall(text)

            if not names:
                continue

            try:
                mod = __import__(submodule, fromlist=names)
            except ImportError:
                continue

            def is_Basic(name):
                cls = getattr(mod, name)
                if hasattr(cls, '_sympy_deprecated_func'):
                    cls = cls._sympy_deprecated_func
                if not isinstance(cls, type):
                    # check instance of singleton class with same name
                    cls = type(cls)
                return issubclass(cls, Basic)

            names = list(filter(is_Basic, names))

            if names:
                modules[submodule] = names

    ns = globals()
    failed = []

    for module, names in modules.items():
        mod = module.replace('.', '__')

        for name in names:
            test = 'test_' + mod + '__' + name

            if test not in ns:
                failed.append(module + '.' + name)

    assert not failed, "Missing classes: %s.  Please add tests for these to sympy/core/tests/test_args.py." % ", ".join(failed)

