
def _base_class_object_build(
    node: nodes.Module | nodes.ClassDef,
    member: type,
    basenames: list[str],
) -> nodes.ClassDef:
    """create astroid for a living class object, with a given set of base names
    (e.g. ancestors)
    """
    name = getattr(member, "__name__", "<no-name>")
    doc = member.__doc__ if isinstance(member.__doc__, str) else None
    klass = build_class(name, node, basenames, doc)
    klass._newstyle = isinstance(member, type)
    try:
        # limit the instantiation trick since it's too dangerous
        # (such as infinite test execution...)
        # this at least resolves common case such as Exception.args,
        # OSError.errno
        if issubclass(member, Exception):
            member_object = member()
            if hasattr(member_object, "__dict__"):
                instdict = member_object.__dict__
            else:
                raise TypeError
        else:
            raise TypeError
    except TypeError:
        pass
    else:
        for item_name, obj in instdict.items():
            valnode = nodes.EmptyNode()
            valnode.object = obj
            valnode.parent = klass
            valnode.lineno = 1
            klass.instance_attrs[item_name] = [valnode]
    return klass

