import copy
from typing import Any

def annotate(
    text: str,
    xy: tuple[Any, Any],
    xytext: tuple[Any, Any] | None = None,
    xycoords: CoordsType = "data",
    textcoords: CoordsType | None = None,
    arrowprops: dict[str, Any] | None = None,
    annotation_clip: bool | None = None,
    **kwargs,
) -> Annotation:
    return gca().annotate(
        text,
        xy,
        xytext=xytext,
        xycoords=xycoords,
        textcoords=textcoords,
        arrowprops=arrowprops,
        annotation_clip=annotation_clip,
        **kwargs,
    )


def annotate(val: Any, type: type) -> Any:
    """
    Annotates a Proxy object with a given type.

    This function annotates a val with a given type if a type of the val is a torch.fx.Proxy object
    Args:
        val (object): An object to be annotated if its type is torch.fx.Proxy.
        type (object): A type to be assigned to a given proxy object as val.
    Returns:
        The given val.
    Raises:
        RuntimeError: If a val already has a type in its node.
    """
    if isinstance(val, Proxy):
        if val.node.type:
            raise RuntimeError(
                f"Tried to annotate a value that already had a type on it!"
                f" Existing type is {val.node.type} "
                f"and new type is {type}. "
                f"This could happen if you tried to annotate a function parameter "
                f"value (in which case you should use the type slot "
                f"on the function signature) or you called "
                f"annotate on the same value twice"
            )
        else:
            val.node.type = type
        return val
    else:
        return val


def annotate(annotation_dict: dict[str, Any]) -> Iterator[None]:
    """
    Temporarily adds custom annotations to the current tracing context.
    The fx_node produced from this tracing context will have the
    custom annotations in node.metadata["custom"] field.

    This context manager allows you to insert arbitrary metadata into the PT2
    tracing system by updating the global `current_meta["custom"]` dictionary.
    The annotations are automatically reverted after the context exits.

    Gradient accumulation nodes will not be annotated.

    This is intended for advanced users who need to attach additional metadata to the fx nodes
    (e.g., for debugging, analysis, or external tooling) during export tracing.

    Note:
        This API is **not backward compatible** and may evolve in future releases.

    Note:
        This API is not compatible with fx.symbolic_trace or jit.trace. It's intended
        to be used with PT2 family of tracers, e.g. torch.export and dynamo.

    Args:
        annotation_dict (dict): A dictionary of custom key-value pairs to inject
            into the FX trace metadata.

    Example:
        After exiting the context, custom annotations are removed.

        >>> with annotate({"source": "custom_pass", "tag": 42}):
        ...     pass  # Your computation here
    """

    global current_meta

    has_custom = "custom" in current_meta
    old_custom = copy.copy(current_meta.get("custom", {}))

    try:
        if not has_custom:
            current_meta["custom"] = dict[str, Any]()

        # Update with all key-value pairs from the input dict
        current_meta["custom"].update(annotation_dict)
        yield
    finally:
        if has_custom:
            # Restore the original custom dict
            current_meta["custom"] = old_custom
        else:
            del current_meta["custom"]


def annotate(the_type, the_value):
    """Use to give type of `the_value` in TorchScript compiler.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.

    This method is a pass-through function that returns `the_value`, used to hint TorchScript
    compiler the type of `the_value`. It is a no-op when running outside of TorchScript.

    Though TorchScript can infer correct type for most Python expressions, there are some cases where
    type inference can be wrong, including:

    - Empty containers like `[]` and `{}`, which TorchScript assumes to be container of `Tensor`
    - Optional types like `Optional[T]` but assigned a valid value of type `T`, TorchScript would assume
      it is type `T` rather than `Optional[T]`

    Note that `annotate()` does not help in `__init__` method of `torch.nn.Module` subclasses because it
    is executed in eager mode. To annotate types of `torch.nn.Module` attributes,
    use :meth:`~torch.jit.Attribute` instead.

    Example:

    .. testcode::

        import torch
        from typing import Dict

        @torch.jit.script
        def fn():
            # Telling TorchScript that this empty dictionary is a (str -> int) dictionary
            # instead of default dictionary type of (str -> Tensor).
            d = torch.jit.annotate(Dict[str, int], {})

            # Without `torch.jit.annotate` above, following statement would fail because of
            # type mismatch.
            d["name"] = 20

    .. testcleanup::

        del fn

    Args:
        the_type: Python type that should be passed to TorchScript compiler as type hint for `the_value`
        the_value: Value or expression to hint type for.

    Returns:
        `the_value` is passed back as return value.
    """
    return the_value


def annotate(f: WrappedFun, in_type: core.InputType | None) -> WrappedFun:
  assert f.in_type is None
  if in_type is None:
    return f
  _check_input_type(in_type)
  return WrappedFun(f.f, f.f_transformed, f.transforms, f.stores, f.params,
                    in_type, f.debug_info)

