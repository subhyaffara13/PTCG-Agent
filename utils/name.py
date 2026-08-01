
def name(pretty: bool = False) -> str:
    """
    Return the name of the current OS distribution, as a human-readable
    string.

    If *pretty* is false, the name is returned without version or codename.
    (e.g. "CentOS Linux")

    If *pretty* is true, the version and codename are appended.
    (e.g. "CentOS Linux 7.1.1503 (Core)")

    **Lookup hierarchy:**

    The name is obtained from the following sources, in the specified order.
    The first available and non-empty value is used:

    * If *pretty* is false:

      - the value of the "NAME" attribute of the os-release file,

      - the value of the "Distributor ID" attribute returned by the lsb_release
        command,

      - the value of the "<name>" field of the distro release file.

    * If *pretty* is true:

      - the value of the "PRETTY_NAME" attribute of the os-release file,

      - the value of the "Description" attribute returned by the lsb_release
        command,

      - the value of the "<name>" field of the distro release file, appended
        with the value of the pretty version ("<version_id>" and "<codename>"
        fields) of the distro release file, if available.
    """
    return _distro.name(pretty)


def name(
    func: FunctionSchema,
    *,
    faithful_name_for_out_overloads: bool = False,
    symint_overload: bool = False,
) -> str:
    name = str(func.name.name)
    if symint_overload:
        name += "_symint"
    if func.is_out_fn():
        if faithful_name_for_out_overloads:
            name += "_outf"
        else:
            name += "_out"

    return name


def name(func: FunctionSchema) -> str:
    return cpp.name(func)


def name(
    g: NativeFunctionsViewGroup,
    *,
    is_reverse: bool,
    include_namespace: bool,
    reapply_views: bool | None = None,
) -> str:
    if reapply_views is None:
        # reapply_views is only important for the fwd lambda,
        # since we always plumb the runtime "reapply_views" argument into the reverse function.
        if not is_reverse:
            raise AssertionError("reapply_views can only be None for reverse")
    if is_reverse:
        return reverse_name(g.view, include_namespace)
    # in the forward case, we just directly call into the at::_ops API (so we always need the namespace)
    if not include_namespace:
        raise AssertionError("include_namespace must be True for forward")
    if g.view_copy is None:
        raise AssertionError("view_copy must be non-None for forward")
    api_name = (
        g.view.func.name.unambiguous_name()
        if reapply_views
        else g.view_copy.func.name.unambiguous_name()
    )
    return f"at::_ops::{api_name}::call"


def name(g: NativeFunctionsGroup) -> str:
    # use the overload name from the functional version
    return str(g.functional.func.name).replace(".", "_")


def name(func: FunctionSchema) -> str:
    name = str(func.name.name)
    # TODO: delete this!
    if func.is_out_fn():
        name += "_out"
    if func.name.overload_name:
        name += f"_{func.name.overload_name}"
    return name


def name(f: NativeFunction) -> str:
    return f.func.name.unambiguous_name()


def name(pretty: bool = False) -> str:
    """
    Return the name of the current OS distribution, as a human-readable
    string.

    If *pretty* is false, the name is returned without version or codename.
    (e.g. "CentOS Linux")

    If *pretty* is true, the version and codename are appended.
    (e.g. "CentOS Linux 7.1.1503 (Core)")

    **Lookup hierarchy:**

    The name is obtained from the following sources, in the specified order.
    The first available and non-empty value is used:

    * If *pretty* is false:

      - the value of the "NAME" attribute of the os-release file,

      - the value of the "Distributor ID" attribute returned by the lsb_release
        command,

      - the value of the "<name>" field of the distro release file.

    * If *pretty* is true:

      - the value of the "PRETTY_NAME" attribute of the os-release file,

      - the value of the "Description" attribute returned by the lsb_release
        command,

      - the value of the "<name>" field of the distro release file, appended
        with the value of the pretty version ("<version_id>" and "<codename>"
        fields) of the distro release file, if available.
    """
    return _distro.name(pretty)


def name(request):
    return request.param

