
def file_info_from_modpath(
    modpath: list[str],
    path: Sequence[str] | None = None,
    context_file: str | None = None,
) -> spec.ModuleSpec:
    """Given a mod path (i.e. split module / package name), return the
    corresponding file.

    Giving priority to source file over precompiled file if it exists.

    :param modpath:
      split module's name (i.e name of a module or package split
      on '.')
      (this means explicit relative imports that start with dots have
      empty strings in this list!)

    :param path:
      optional list of path where the module or package should be
      searched (use sys.path if nothing or None is given)

    :param context_file:
      context file to consider, necessary if the identifier has been
      introduced using a relative import unresolvable in the actual
      context (i.e. modutils)

    :raise ImportError: if there is no such module in the directory

    :return:
      the path to the module's file or None if it's an integrated
      builtin module such as 'sys'
    """
    if context_file is not None:
        context: str | None = os.path.dirname(context_file)
    else:
        context = context_file
    if modpath[0] == "xml":
        # handle _xmlplus
        try:
            return _spec_from_modpath(["_xmlplus", *modpath[1:]], path, context)
        except ImportError:
            return _spec_from_modpath(modpath, path, context)
    elif modpath == ["os", "path"]:
        # FIXME: currently ignoring search_path...
        return spec.ModuleSpec(
            name="os.path",
            location=os.path.__file__,
            type=spec.ModuleType.PY_SOURCE,
        )
    return _spec_from_modpath(modpath, path, context)

