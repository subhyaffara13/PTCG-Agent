
def _gi_build_stub(parent):  # noqa: C901
    """
    Inspect the passed module recursively and build stubs for functions,
    classes, etc.
    """
    # pylint: disable = too-many-branches, too-many-statements

    classes = {}
    functions = {}
    constants = {}
    methods = {}
    for name in dir(parent):
        if name.startswith("__") and name not in _special_methods:
            continue

        # Check if this is a valid name in python
        if not re.match(_identifier_re, name):
            continue

        try:
            obj = getattr(parent, name)
        except Exception:  # pylint: disable=broad-except
            # gi.module.IntrospectionModule.__getattr__() can raise all kinds of things
            # like ValueError, TypeError, NotImplementedError, RepositoryError, etc
            continue

        if inspect.isclass(obj):
            classes[name] = obj
        elif inspect.isfunction(obj) or inspect.isbuiltin(obj):
            functions[name] = obj
        elif inspect.ismethod(obj) or inspect.ismethoddescriptor(obj):
            methods[name] = obj
        elif (
            str(obj).startswith("<flags")
            or str(obj).startswith("<enum ")
            or str(obj).startswith("<GType ")
            or inspect.isdatadescriptor(obj)
        ):
            constants[name] = 0
        elif isinstance(obj, (int, str)):
            constants[name] = obj
        elif callable(obj):
            # Fall back to a function for anything callable
            functions[name] = obj
        else:
            # Assume everything else is some manner of constant
            constants[name] = 0

    ret = ""

    if constants:
        ret += f"# {parent.__name__} constants\n\n"
    for name in sorted(constants):
        if name[0].isdigit():
            # GDK has some busted constant names like
            # Gdk.EventType.2BUTTON_PRESS
            continue

        val = constants[name]

        strval = str(val)
        if isinstance(val, str):
            strval = '"%s"' % str(val).replace("\\", "\\\\")
        ret += f"{name} = {strval}\n"

    if ret:
        ret += "\n\n"
    if functions:
        ret += f"# {parent.__name__} functions\n\n"
    for name in sorted(functions):
        ret += f"def {name}(*args, **kwargs):\n"
        ret += "    pass\n"

    if ret:
        ret += "\n\n"
    if methods:
        ret += f"# {parent.__name__} methods\n\n"
    for name in sorted(methods):
        ret += f"def {name}(self, *args, **kwargs):\n"
        ret += "    pass\n"

    if ret:
        ret += "\n\n"
    if classes:
        ret += f"# {parent.__name__} classes\n\n"
    for name, obj in sorted(classes.items()):
        base = "object"
        if issubclass(obj, Exception):
            base = "Exception"
        ret += f"class {name}({base}):\n"

        classret = _gi_build_stub(obj)
        if not classret:
            classret = "pass\n"

        for line in classret.splitlines():
            ret += "    " + line + "\n"
        ret += "\n"

    return ret

