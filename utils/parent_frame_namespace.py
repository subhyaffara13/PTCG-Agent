
def parent_frame_namespace(*, parent_depth: int = 2, force: bool = False) -> dict[str, Any] | None:
    """Fetch the local namespace of the parent frame where this function is called.

    Using this function is mostly useful to resolve forward annotations pointing to members defined in a local namespace,
    such as assignments inside a function. Using the standard library tools, it is currently not possible to resolve
    such annotations:

    ```python {lint="skip" test="skip"}
    from typing import get_type_hints

    def func() -> None:
        Alias = int

        class C:
            a: 'Alias'

        # Raises a `NameError: 'Alias' is not defined`
        get_type_hints(C)
    ```

    Pydantic uses this function when a Pydantic model is being defined to fetch the parent frame locals. However,
    this only allows us to fetch the parent frame namespace and not other parents (e.g. a model defined in a function,
    itself defined in another function). Inspecting the next outer frames (using `f_back`) is not reliable enough
    (see https://discuss.python.org/t/20659).

    Because this function is mostly used to better resolve forward annotations, nothing is returned if the parent frame's
    code object is defined at the module level. In this case, the locals of the frame will be the same as the module
    globals where the class is defined (see `_namespace_utils.get_module_ns_of`). However, if you still want to fetch
    the module globals (e.g. when rebuilding a model, where the frame where the rebuild call is performed might contain
    members that you want to use for forward annotations evaluation), you can use the `force` parameter.

    Args:
        parent_depth: The depth at which to get the frame. Defaults to 2, meaning the parent frame where this function
            is called will be used.
        force: Whether to always return the frame locals, even if the frame's code object is defined at the module level.

    Returns:
        The locals of the namespace, or `None` if it was skipped as per the described logic.
    """
    frame = sys._getframe(parent_depth)

    if frame.f_code.co_name.startswith('<generic parameters of'):
        # As `parent_frame_namespace` is mostly called in `ModelMetaclass.__new__`,
        # the parent frame can be the annotation scope if the PEP 695 generic syntax is used.
        # (see https://docs.python.org/3/reference/executionmodel.html#annotation-scopes,
        # https://docs.python.org/3/reference/compound_stmts.html#generic-classes).
        # In this case, the code name is set to `<generic parameters of MyClass>`,
        # and we need to skip this frame as it is irrelevant.
        frame = cast(types.FrameType, frame.f_back)  # guaranteed to not be `None`

    # note, we don't copy frame.f_locals here (or during the last return call), because we don't expect the namespace to be
    # modified down the line if this becomes a problem, we could implement some sort of frozen mapping structure to enforce this.
    if force:
        return frame.f_locals

    # If either of the following conditions are true, the class is defined at the top module level.
    # To better understand why we need both of these checks, see
    # https://github.com/pydantic/pydantic/pull/10113#discussion_r1714981531.
    if frame.f_back is None or frame.f_code.co_name == '<module>':
        return None

    return frame.f_locals

